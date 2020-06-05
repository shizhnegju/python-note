import json
import jwt
from operator import itemgetter

from django.contrib.auth.hashers import check_password
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.views import APIView
from rock.basic import CassResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import UserProfile, Menu, Role
from ..serializers.user_serializer import UserListSerializer, UserCreateSerializer, UserModifySerializer, \
    UserInfoListSerializer
from ..serializers.menu_serializer import MenuSerializer
from common.custom import CommonPagination, RbacPermission
from rock.settings import SECRET_KEY, BASE_API
from rock.code import *

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserAuthView(APIView):
    """
    用户认证获取token
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            return Response({"data": {'access': jwt.encode(payload, SECRET_KEY)}, "code": 20000, "message": "success",
                             "detail": {'token': jwt.encode(payload, SECRET_KEY)}}, status=OK)
        else:
            return Response('用户名或密码错误!', status=BAD)


class UserChangePassword(APIView):
    """
    修改密码
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = UserProfile.objects.get(username=username)
        user.set_password(password)
        user.save()
        return CassResponse("ok", status=OK)


class UserInfoView(APIView):
    """
    获取当前用户信息和权限
    """

    @classmethod
    def get_permission_from_role(cls, request):
        try:
            if request.user:
                perms_list = []
                for item in request.user.roles.values('permissions__method').distinct():
                    perms_list.append(item['permissions__method'])
                return perms_list
        except AttributeError:
            return None

    @classmethod
    def get__role_name(cls, request):
        try:
            if request.user:
                role_name_list = []
                for item in request.user.roles.values('name').distinct():
                    role_name_list.append(item['name'])
                return role_name_list
        except AttributeError:
            return None

    def get(self, request):
        if request.user.id is not None:
            perms = self.get_permission_from_role(request)
            role_name = self.get__role_name(request)
            data = {
                'id': request.user.id,
                'username': request.user.username,
                'name': request.user.name,
                'avatar': BASE_API + "/be-media/img/db_234.gif",
                'email': request.user.email,
                'is_active': request.user.is_active,
                'createTime': request.user.date_joined,
                'roles_name': role_name,
                'roles': perms,
            }
            return CassResponse(data, status=OK)
        else:
            return CassResponse('请登录后访问!', status=FORBIDDEN)


class UserBuildMenuView(APIView):
    """
    绑定当前用户菜单信息
    """

    def get_menu_from_role(self, request):
        if request.user:
            menu_dict = {}
            menus = request.user.roles.values(
                'menus__id',
                'menus__name',
                'menus__path',
                'menus__is_frame',
                'menus__is_show',
                'menus__component',
                'menus__icon',
                'menus__sort',
                'menus__pid'
            ).distinct()
            for item in menus:
                if item['menus__id']:
                    if item['menus__pid'] is None:
                        if item['menus__is_frame']:
                            # 判断是否外部链接
                            top_menu = {
                                'id': item['menus__id'],
                                'path': item['menus__path'],
                                'component': 'Layout',
                                'children': [{
                                    'path': item['menus__path'],
                                    'meta': {
                                        'title': item['menus__name'],
                                        'icon': item['menus__icon']
                                    }
                                }],
                                'pid': item['menus__pid'],
                                'sort': item['menus__sort']
                            }
                        else:
                            top_menu = {
                                'id': item['menus__id'],
                                'name': item['menus__name'],
                                'path': '/' + item['menus__path'],
                                'redirect': 'noredirect',
                                'component': 'Layout',
                                'alwaysShow': True,
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon']
                                },
                                'pid': item['menus__pid'],
                                'sort': item['menus__sort'],
                                'children': []
                            }
                        menu_dict[item['menus__id']] = top_menu
                    else:
                        if item['menus__is_frame']:
                            children_menu = {
                                'id': item['menus__id'],
                                'name': item['menus__name'],
                                'path': item['menus__path'],
                                'component': 'Layout',
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon'],
                                },
                                'pid': item['menus__pid'],
                                'sort': item['menus__sort']
                            }
                        elif item['menus__is_show']:
                            children_menu = {
                                'id': item['menus__id'],
                                'name': item['menus__name'],
                                'path': item['menus__path'],
                                'component': item['menus__component'],
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon'],
                                },
                                'pid': item['menus__pid'],
                                'sort': item['menus__sort']
                            }
                        else:
                            children_menu = {
                                'id': item['menus__id'],
                                'name': item['menus__name'],
                                'path': item['menus__path'],
                                'component': item['menus__component'],
                                'meta': {
                                    'title': item['menus__name'],
                                    'noCache': True,
                                },
                                'hidden': True,
                                'pid': item['menus__pid'],
                                'sort': item['menus__sort']
                            }
                        menu_dict[item['menus__id']] = children_menu
            return menu_dict

    def get_all_menu_dict(self):
        '''
        获取所有菜单数据，重组结构
        '''
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        tree_dict = {}
        for item in serializer.data:
            if item['pid'] is None:
                if item['is_frame']:
                    # 判断是否外部链接
                    top_menu = {
                        'id': item['id'],
                        'path': item['path'],
                        'component': 'Layout',
                        'children': [{
                            'path': item['path'],
                            'meta': {
                                'title': item['name'],
                                'icon': item['icon']
                            }
                        }],
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    top_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': '/' + item['path'],
                        'redirect': 'noredirect',
                        'component': 'Layout',
                        'alwaysShow': True,
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon']
                        },
                        'pid': item['pid'],
                        'sort': item['sort'],
                        'children': []
                    }
                tree_dict[item['id']] = top_menu
            else:
                if item['is_frame']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': 'Layout',
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                elif item['is_show']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'noCache': True,
                        },
                        'hidden': True,
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                tree_dict[item['id']] = children_menu
        return tree_dict

    def get_all_menus(self, request):
        try:
            perms = UserInfoView.get_permission_from_role(request)
            tree_data = []
            if 'admin' in perms or request.user.is_superuser:
                tree_dict = self.get_all_menu_dict()
            else:
                tree_dict = self.get_menu_from_role(request)
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('redirect', 'noredirect')
                    parent.setdefault('alwaysShow', True)
                    parent.setdefault('children', []).append(tree_dict[i])
                    parent['children'] = sorted(parent['children'], key=itemgetter('sort'))
                else:
                    tree_data.append(tree_dict[i])
        except Exception as e:
            return "error"
        return tree_data

    def get(self, request):
        if request.user.id is not None:
            menu_data = self.get_all_menus(request)
            if menu_data == "error":
                return CassResponse('无一级菜单访问权限!', status=BAD)
            return CassResponse(menu_data, status=OK)
        else:
            return CassResponse('请登录后访问!', status=FORBIDDEN)


class UserViewSet(ModelViewSet):
    """
    用户管理：增删改查
    """
    perms_map = ({'*': 'admin'}, {'*': 'user_all'}, {'get': 'user_list'}, {'post': 'user_create'}, {'put': 'user_edit'},
                 {'delete': 'user_delete'})
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('is_active',)
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        # 创建用户默认添加密码
        request.data['password'] = '123456'
        request.data['is_active'] = True
        if not request.data['roles']:
            request.data['roles'] = [2]  # 默认角色
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CassResponse(serializer.data, status=CREATED, headers=headers)

    # def destroy(self, request, *args, **kwargs):
    #     # 删除用户时删除其他表关联的用户
    #     instance = self.get_object()
    #     id = str(kwargs['pk'])
    #     compile_manages = CompileManagement.objects.filter(
    #         Q(users__id__icontains=id + ',') | Q(users__id__in=id) | Q(users__id__endswith=',' + id)).values()
    #     if compile_manages:
    #         for compile_manage in compile_manages:
    #             print(compile_manage)
    #             user_id = compile_manage['users__id'].split(',')
    #             user_id.remove(id)
    #             user_id = ','.join(user_id)
    #             CompileManagement.objects.filter(id=compile_manage['id']).update(users_id=user_id)
    #     ConnectionInfo.objects.filter(uid_id=id).delete()
    #     self.perform_destroy(instance)
    #     return XopsResponse(status=NO_CONTENT)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated],
            url_path='change-passwd', url_name='change-passwd')
    def set_password(self, request, pk=None):
        perms = UserInfoView.get_permission_from_role(request)
        user = UserProfile.objects.get(id=pk)
        if 'admin' in perms or 'user_all' in perms or request.user.is_superuser:
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password2']
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
                return CassResponse('密码修改成功!')
            else:
                return CassResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
        else:
            old_password = request.data['old_password']
            if check_password(old_password, user.password):
                new_password1 = request.data['new_password1']
                new_password2 = request.data['new_password2']
                if new_password1 == new_password2:
                    user.set_password(new_password2)
                    user.save()
                    return CassResponse('密码修改成功!')
                else:
                    return CassResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
            else:
                return CassResponse('旧密码错误!', status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for s_data in serializer.data:
                s_data['image'] = BASE_API + "/be-media/img/db_234.gif"
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for s_data in serializer.data:
            s_data['image'] = BASE_API + "/be-media/img/db_234.gif"
        return Response(serializer.data)


class UserListView(ListAPIView):
    """
    用户列表
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserInfoListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name', 'roles')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
