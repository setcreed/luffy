from django.urls import path, re_path, include

from . import views
from utils.router import router
router.register('categories', views.CategoryListViewSet, basename='category')
router.register('free', views.FreeCourseListViewSet, basename='free-course')

urlpatterns = [
    path('', include(router.urls)),
]
