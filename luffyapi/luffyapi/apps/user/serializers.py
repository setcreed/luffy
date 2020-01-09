import re
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache
from django.conf import settings
from . import models


class LoginModelSerializer(serializers.ModelSerializer):
    # post请求，序列化默认当做create动作进行校验，需要校验数据库，create动作username会抛用户已存在异常
    # 抛用户已存在异常是多余的，所以自定义系统校验规则即可
    username = serializers.CharField(min_length=3, max_length=16)
    password = serializers.CharField(min_length=3, max_length=16)

    class Meta:
        model = models.User
        fields = ('username', 'password')

    # 用全局钩子，完成token的签发
    def validate(self, attrs):
        # 1）通过 username 和 password 完成多方式登录校验，得到user对象
        user = self._validate_user(attrs)
        # 2）user对象包装payload载荷
        payload = jwt_payload_handler(user)
        # 3）payload载荷签发token
        token = jwt_encode_handler(payload)
        # 4）将user与token存储到serializer对象中，方便在视图类中使用
        self.content = {
            'user': user,
            'token': token
        }
        return attrs

    def _validate_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if re.match(r'.*@.*', username):  # 邮箱
            user = models.User.objects.filter(email=username).first()  # type: models.User
        elif re.match(r'^1[3-9][0-9]{9}$', username):  # 电话
            user = models.User.objects.filter(mobile=username).first()
        else:  # 用户名
            user = models.User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({'message': '用户信息异常'})

        return user



class LoginMobileModelSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(min_length=11, max_length=11)
    code = serializers.CharField(min_length=6, max_length=6)

    class Meta:
        model = models.User
        fields = ('mobile', 'code')

    # 验证码格式内容有误就不需要进行 取服务器存储的验证码(IO操作) 进行校验
    def validate_code(self, value):
        try:
            int(value)
            return value
        except:
            raise serializers.ValidationError('验证码有误')

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.pop('code')
        # 拿服务器缓存的验证码
        old_code = cache.get(settings.SMS_CACHE_FORMAT % mobile)

        if code != old_code:
            raise serializers.ValidationError({'code': '验证码有误'})

        # 验证码校验通过，验证码失效（验证码一次性使用）
        # cache.set(settings.SMS_CACHE_FORMAT % mobile, None, 0)

        try:
            user = models.User.objects.get(mobile=mobile, is_active=True)
        except:
            raise serializers.ValidationError({'mobile': '该用户不存在'})

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.content = {
            'user': user,
            'token': token
        }
        return attrs


class RegisterMobileModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, min_length=6, max_length=6)

    class Meta:
        model = models.User
        fields = ('username', 'mobile', 'password', 'code')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'username': {
                'read_only': True
            }
        }

    # 每一个反序列化字段都要可以配置一个局部钩子
    def validate_mobile(self, value):
        if not re.match(r'^1[3-9][0-9]{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    def validate_code(self, value):
        try:
            int(value)
            return value
        except:
            raise serializers.ValidationError('验证码有误')

    # 全局校验
    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.pop('code')
        old_code = cache.get(settings.SMS_CACHE_FORMAT % mobile)
        if code != old_code:
            raise serializers.ValidationError({'code': '验证码有误'})

        # 验证码校验通过，验证码失效（验证码一次性使用）
        cache.set(settings.SMS_CACHE_FORMAT % mobile, None, 0)

        # 创建用户需要一些额外的信息，比如username
        attrs['username'] = mobile

        return attrs

    # create方法是是需要重写：默认入库，密码是明文
    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
