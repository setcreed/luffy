from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.conf import settings
from utils.response import APIResponse
from . import models, serializers
from rest_framework.response import Response
from django.core.cache import cache
class BannerListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('-orders').all()[:settings.BANNER_COUNT]
    serializer_class = serializers.BannerModelSerializer

    # 自定义响应结果的格式
    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     return APIResponse(results=response.data)

    # 接口缓存
    def list(self, request, *args, **kwargs):
        data = cache.get('banner_cache')

        if not data:
            print('走了数据库')
            response = super().list(request, *args, **kwargs)
            cache.set('banner_cache', response.data)  # 不设置过期时间，缓存的更新在后台异步更新(celery异步框架)
            return response

        return Response(data)


