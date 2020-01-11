from .celery import app
# 获取项目中的模型类
from home.models import Banner
from django.core.cache import cache
from django.conf import settings
from home.serializers import BannerModelSerializer

@app.task
def update_banner_cache():
    banner_query = Banner.objects.filter(is_delete=False, is_show=True).all()[:settings.BANNER_COUNT]
    banner_data = BannerModelSerializer(banner_query, many=True).data
    for banner in banner_data:
        banner['image'] = '%s%s' % (settings.BASE_URL, banner.get('image'))
    cache.set('banner_cache', banner_data)
    return True
