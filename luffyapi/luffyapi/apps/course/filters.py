from django_filters.filterset import FilterSet
from django_filters import filters
from . import models
class CourseFilterSet(FilterSet):
    # 实现区间：field_name关联model表属性，lookup_expr设置过滤规则
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    class Meta:
        model = models.Course
        # min_price 和 max_price 自定义规则字段可以不在fields中配置
        fields = ['course_category']



# 自定义过滤器：自定义普通类，实现filter_queryset可以接受request, queryset, view返回过滤处理后的queryset即可
class MyFilter:
    def filter_queryset(self, request, queryset, view):
        # 过滤条件是死的，?count=数字，也可以写高级一点，从view中去反射配置信息，或者将配置信息放在settings中
        count = request.query_params.get('count', None)
        if not count:
            return queryset  # 没过滤
        try:
            count = int(count)
            return queryset[:count]  # 过滤
        except:
            return queryset  # 没过滤


