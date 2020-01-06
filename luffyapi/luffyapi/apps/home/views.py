from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from . import models, serializers
from utils.response import APIResponse
from django.conf import settings

class BannerListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('-orders').all()[:settings.BANNER_COUNT]
    serializer_class = serializers.BannerModelSerializer

    # # 自定义响应
    # def list(self, request, *args, **kwargs):
    #     response = super().initial(request, *args, **kwargs)
    #     return APIResponse(results=response.data)

