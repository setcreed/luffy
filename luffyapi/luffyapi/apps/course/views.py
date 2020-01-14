from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from . import models, serializers
class CategoryListViewSet(ListModelMixin, GenericViewSet):
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CategoryModelSerializer


# 过滤组件：分页、搜索、排序、分类、区间

# 自定义分页组件
from . import paginations
# drf默认提供两个过滤组件：排序、搜索
from rest_framework.filters import SearchFilter, OrderingFilter

# drf默认不能完成 分类、区间 两种过滤，需要借助第三方插件：pip install django-filter
from django_filters.rest_framework import DjangoFilterBackend
# 自定义规则类
from .filters import CourseFilterSet, MyFilter
class FreeCourseViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CourseModelSerializer

    # 走系统分页类
    # pagination_class = pagination.PageNumberPagination
    # pagination.PageNumberPagination.page_size = 2

    # 走自定义分页类
    pagination_class = paginations.PageNumberPagination
    # pagination_class = paginations.LimitOffsetPagination

    # 注：接口分页前后，response的格式不一样
    #       分页前：数据是response.data
    #       分页后：数据是response.data.results


    # """
    # 过滤类：有filter_queryset(self, request, queryset, view)方法，返回值是queryset
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # SearchFilter组件：
    #   参与全文搜索的字段为name和brief（两个字段必须都是数据库表字段）
    #   接口：?search=搜索关键字，会全文匹配name和brief两个字段
    search_fields = ['name', 'brief']
    # OrderingFilter组件：
    #   参与排序字段为price、id和students（三个字段必须都是数据库表字段）
    #   接口：
    #       ?ordering=price 按价格升序
    #       ?ordering=-price 按价格降序
    #       ?ordering=id 按主键升序
    #       ?ordering=-price,id 按价格降序，价格相同时按主键升序
    ordering_fields = ['price', 'id', 'students']

    # django-filter插件的DjangoFilterBackend组件：
    # 第一种配置，配置字段：
    # filter_fields = ['course_category']
    # 第二个配置，配置类
    filter_class = CourseFilterSet
    # """

    """自定义过滤器
    filter_backends = [MyFilter]
    """

class SearchCourseListViewSet(ListModelMixin, GenericViewSet):
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CourseModelSerializer

    filter_backends = [SearchFilter]
    search_fields = ['name']

    pagination_class = paginations.PageNumberPagination


class CourseChapterViewSet(ListModelMixin, GenericViewSet):
    queryset = models.CourseChapter.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CourseChapterModelSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']
