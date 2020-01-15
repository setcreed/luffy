from rest_framework import serializers
from . import models
from course.models import Course
class OrderModelSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(required=True, queryset=Course.objects.all(), many=True)
    class Meta:
        model = models.Order
        fields = ['subject', 'total_amount', 'pay_type', 'courses']
        extra_kwargs = {
            'total_amount': {
                'required': True
            },
            'pay_type': {
                'required': True
            }
        }

    def validate(self, attrs):
        # 1）总价校验
        total_amount = self._check_total_amount(attrs)
        # 2）订单号的生成
        out_trade_no = self._get_out_trade_no()
        # 3）支付用户
        user = self._get_request_user()
        # 4）生成支付链接
        pay_url = self._get_pay_url(out_trade_no, total_amount, attrs.get('subject'))

        # 5）支付链接要在视图类中返回给前台，所以要通过序列化类传给视图类
        self.pay_url = pay_url  # 在视图类中用对象 serializer.pay_url

        # 6）订单与订单详情入库的额外信息，需要添加给attrs
        attrs['out_trade_no'] = out_trade_no
        attrs['user'] = user

        # 7）校验通过，返回attrs
        return attrs


    def create(self, validated_data):
        # print(validated_data)
        courses = validated_data.pop('courses')  # 订单详情表入库才需要
        # 订单表记录生成
        order_obj = models.Order.objects.create(**validated_data)
        # 订单详情表记录生成
        for course in courses:
            models.OrderDetail.objects.create(order=order_obj, course=course, price=course.price, real_price=course.price)
        return order_obj

    # 内部使用的方法
    # 总价校验
    def _check_total_amount(self, attrs):
        # 前台总价
        total_amount = attrs.get('total_amount')
        # 后台总价
        total_amount_temp = 0
        courses = attrs.get('courses')
        for course in courses:
            total_amount_temp += course.price
        # 总价校验，可能出现小数影响判断结果
        if total_amount != total_amount_temp:
            raise serializers.ValidationError({'total_amount': '价格异常'})
        return total_amount

    def _get_out_trade_no(self):
        import time
        temp_no = '%.7f' % time.time()
        out_trade_no = temp_no.replace('.', '')
        return out_trade_no[-13: -1]

    def _get_request_user(self):
        return self.context.get('request').user

    def _get_pay_url(self, out_trade_no, total_amount, subject):
        from libs.iPay import alipay, alipay_gateway
        from django.conf import settings
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,
            total_amount=str(total_amount),
            subject=subject,
            return_url=settings.RETURN_URL,  # 同步回调：前台回调接口
            notify_url=settings.NOTIFY_URL  # 异步回调：后台回调接口
        )
        return alipay_gateway + order_string



