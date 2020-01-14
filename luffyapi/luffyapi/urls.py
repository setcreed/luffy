from django.urls import path, re_path, include

from django.views.static import serve
from django.conf import settings

# from django.contrib import admin
# xadmin的依赖
import xadmin
xadmin.autodiscover()

# xversion模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    # 后台管理
    path('xadmin/', xadmin.site.urls),

    # 路由分发
    path('user/', include('user.urls')),
    path('home/', include('home.urls')),
    path('course/', include('course.urls')),

    # 媒体文件
    re_path('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
