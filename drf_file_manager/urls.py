from django.urls import path, include
from rest_framework import routers

from .views import FileViewSet


router = routers.DefaultRouter()
router.register('', FileViewSet, basename='file-manager')

urlpatterns = router.urls
