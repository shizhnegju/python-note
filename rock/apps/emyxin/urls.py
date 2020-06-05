from django.urls import path, include
from rest_framework import routers
from emyxin import views

router = routers.SimpleRouter()
router.register(r'checkin', views.CheckinViewSet)

urlpatterns = [
    path(r"", include(router.urls)),
]
