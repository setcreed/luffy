from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from . import serializers, models

class CategoryListViewSet(ListModelMixin, GenericViewSet):
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CategoryModelSerializer


class FreeCourseListViewSet(ListModelMixin, GenericViewSet):
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CourseModelSerializer