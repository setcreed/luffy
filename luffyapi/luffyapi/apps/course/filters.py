from rest_framework import filters
from django_filters.filterset import FilterSet
from django_filters import filters
from . import models

class MyFilter:
    def filter_queryset(self, request, queryset, view):
        count = request.query_params.get('count', None)
        if not count:
            return queryset   # 没有过滤

        try:
            count = int(count)
            return queryset[:count]  # 过滤了
        except:
            return queryset   # 没有过滤


class CourseFilterSet(FilterSet):
    # 实现区间：field_name关联model表属性，lookup_expr设置过滤规则

    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    class Meta:
        model = models.Course
        # min_price和max_price 自定义规则字段可以不在fields配置
        fields = ['course_category']