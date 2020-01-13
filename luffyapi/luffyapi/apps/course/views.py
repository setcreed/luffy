from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from . import serializers, models

from rest_framework.filters import OrderingFilter, SearchFilter

class CategoryListViewSet(ListModelMixin, GenericViewSet):
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CategoryModelSerializer


from . import paginations
from . import filters

from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseFilterSet

class FreeCourseListViewSet(ListModelMixin, GenericViewSet):
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CourseModelSerializer

    # pagination_class = pagination.PageNumberPagination
    # pagination.PageNumberPagination.page_size = 2
    pagination_class = paginations.PageNumberPagination
    # pagination_class = paginations.LimitOffsetPagination
    # pagination_class = paginations.CursorPagination



    # 过滤类：有filter_queryset(self, request, queryset, view)方法，返回值是queryset
    # 配置搜索组件
    # filter_backends = [SearchFilter]
    # # 配置参与搜索字段
    # search_fields = ['name', 'brief']

    # # 配置排序组件
    # filter_backends = [OrderingFilter]
    # # 配置参与排序字段
    # ordering_fields = ['price', 'id', 'students']

    # filter_backends = [filters.MyFilter]

    # 配置过滤组件
    filter_backends = [DjangoFilterBackend]
    # 配置过滤规则的类，配置filterset_class 或 filter_class 均可
    # 第一种配置，配置字段：
    # filter_fields = ['course_category']
    # 第二个配置，配置类
    filter_class = CourseFilterSet




