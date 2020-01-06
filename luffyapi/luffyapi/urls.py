# from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings

import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    path('user/', include('user.urls')),
    path('home/', include('home.urls')),

    re_path('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
