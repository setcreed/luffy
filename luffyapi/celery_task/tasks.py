from .celery import app

from user.models import User

# 测试django环境下的任务
@app.task
def get_users():
    user_list = User.objects.all()
    print(user_list)
    return True

# 伪代码：立即和延迟任务使用
@app.task
def send_email(user, content):
    result = print('对user发送content邮件内容')
    if not result:
        print('短信推送用户，邮件发送失败')
        return False
    return True

# 案例：django异步更新缓存
from home.models import Banner
from django.conf import settings
from django.core.cache import cache
from home.serializers import BannerModelSerializer
@app.task
def update_banner_cache():
    banner_query = Banner.objects.filter(is_delete=False, is_show=True).order_by('-orders').all()[:settings.BANNER_COUNT]
    banner_data = BannerModelSerializer(banner_query, many=True).data
    for banner in banner_data:
        banner['image'] = "%s%s" % (settings.BASE_URL, banner.get('image'))
    cache.set('banner_cache', banner_data)
    return True



