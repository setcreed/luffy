import re

from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView

from libs import tx_sms
from utils.response import APIResponse
from . import serializers, models, throttles


# 多方式登录
class LoginAPIView(APIView):
    # 认证权限一定要局部禁用
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 内部在全局钩子中完成token的签发
        return APIResponse(results={
            'username': serializer.content.get('user').username,
            'token': serializer.content.get('token')
        })


# 手机验证码登录
class LoginMobileAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginMobileModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return APIResponse(results={
            'username': serializer.content.get('user').username,
            'token': serializer.content.get('token')
        })


# 发送验证码
class SMSAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    throttle_classes = [throttles.SMSRateThrottle]

    def post(self, request, *args, **kwargs):
        # 1）处理手机号
        mobile = request.data.get('mobile', None)
        if not mobile:
            return APIResponse(1, msg='mobile字段必须', http_status=400)

        if not re.match(r'^1[3-9][0-9]{9}$', mobile):
            return APIResponse(1, msg='mobile格式有误', http_status=400)

        # 2) 生成验证码
        code = tx_sms.get_sms_code()

        # 3）发送验证码
        result = tx_sms.send_sms(mobile, code, settings.SMS_EXP // 60)

        if not result:
            return APIResponse(1, msg='验证码发送失败')

        # 4）缓存验证码
        cache.set(settings.SMS_CACHE_FORMAT % mobile, code, settings.SMS_EXP)

        # 5）成功响应
        return APIResponse(0, msg='验证码发送成功')


# 手机号验证是否注册了
class MobileCheckAPIView(APIView):
    def get(self, request, *args, **kwargs):
        mobile = request.query_params.get('mobile')
        if not mobile:
            return APIResponse(1, 'mobile必须提供', http_status=400)
        if not re.match(r'^1[3-9][0-9]{9}$', mobile):
            return APIResponse(1, msg='mobile格式有误', http_status=400)
        try:
            # 只要数据库有，就代表已注册
            models.User.objects.get(mobile=mobile)
            return APIResponse(2, msg='手机号已注册')
        except:
            return APIResponse(0, msg='手机号未注册')


# 手机号验证码注册
class RegisterMobileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.RegisterMobileModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        return APIResponse(results=serializers.RegisterMobileModelSerializer(user_obj).data)
