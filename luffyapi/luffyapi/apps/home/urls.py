from django.urls import path, re_path, include
from utils.router import router

from . import views
router.register('banners', views.BannerListViewSet, basename='banner')

urlpatterns = [
    re_path(r'', include(router.urls))
]
