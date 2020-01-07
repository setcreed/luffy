from rest_framework.views import APIView
from . import serializer
from utils.response import APIResponse

import re

# 多方式登录
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializers = serializer.LoginModelSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)  # 内部在全局钩子中完成token的签发
        print(serializers.content)
        return APIResponse(results={
            'username': serializers.content.get('user').username,
            'token': serializers.content.get('token')
        })


# 手机验证码登录
class LoginMobileAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializers = serializer.LoginModelMobileSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)  # 内部在全局钩子中完成token的签发
        print(serializers.content)
        return APIResponse(results={
            'username': serializers.content.get('user').username,
            'token': serializers.content.get('token')
        })


# 发送验证码
from libs import tx_sms
from django.core.cache import cache
from django.conf import settings
class SMSAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 1、处理手机号
        mobile = request.data.get('mobile', None)
        if not mobile:
            return APIResponse(1, msg='mobile字段错误', http_status=400)

        if not re.match(r'^1[1-9][0-9]{9}$', mobile):
            return APIResponse(1, msg='mobile格式错误', http_status=400)

        # 2、生成验证码
        code = tx_sms.get_sms_code()

        # 3、发送验证码
        result = tx_sms.send_sms(mobile, code, settings.SMS_EXP // 60)
        if not result:
            return APIResponse(1, msg='验证码发送失败')

        # 4、缓存验证码
        cache.set(settings.SMS_CACHE_FORMAT % mobile, code, settings.SMS_EXP)

        # 5、成功响应
        return APIResponse(0, msg='验证码发送成功')



