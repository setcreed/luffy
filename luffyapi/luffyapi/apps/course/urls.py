from django.urls import path, re_path, include
from . import views

from utils.router import router

router.register('categories', views.CategoryListViewSet, 'category')
router.register('free', views.FreeCourseViewSet, 'free-course')
router.register('search', views.SearchCourseListViewSet, 'search-course')
router.register('chapters', views.CourseChapterViewSet, 'chapter')

urlpatterns = [
    path('', include(router.urls)),
]
