import logging

from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.custom import RbacPermission, CommonPagination
from emyxin.models import checkinlist
from emyxin.serializers import CheckinlistSerializer

from rest_framework.response import Response
from rest_framework import status
import requests
import json

info_logger = logging.getLogger('info')


# Create your views here.
class CheckinViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (RbacPermission,)
    pagination_class = CommonPagination
    queryset = checkinlist.objects.all()
    serializer_class = CheckinlistSerializer

    def create(self, request, *args, **kwargs):
        info_logger.info("新增签到数据")
        savedata = request.data
        info_logger.info("新的签到数据是：", savedata)
        scode = savedata['code']
        secretcode = self._getSecret(scode)
        info_logger.info("secretcode数据：", secretcode)
        if 'openid' in secretcode:
            new_uuid = secretcode['openid']
            savedata['unid'] = new_uuid
        else:
            return Response(secretcode, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=savedata)
        if serializer.is_valid():
            serializer.save()
            info_logger.info("添加新的签到数据成功")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _getSecret(self, code):
        data = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxeaf2c5aa3ac7dad2&secret=7071e10b2f452d7b899d7dae06022ef9&js_code=' + code + '&grant_type=authorization_code'
        r = requests.get(url=data)  # 最基本的GET请求
        return json.loads(r.text)
