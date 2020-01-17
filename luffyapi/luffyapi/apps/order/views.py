from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from . import models, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class OrderAPIView(CreateAPIView):
    # 必须登录才能访问
    permission_classes = [IsAuthenticated]

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 修改返回信息
        return Response(serializer.pay_url)


from libs.iPay import alipay
from utils.logging import logger


class OrderSuccessAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response('后台接受到同步信息了')
        # params = request.query_params
        # print(params)


    # 支付宝异步回调逻辑
    def post(self, request, *args, **kwargs):
        # 订单校验成功后修改订单信息（post异步回调的逻辑）
        data = request.data.dict()
        # QueryDict类型没有pop方法，request.query_params.dict()和request.data.dict() 都能直接转化为dict类型
        sign = data.pop('sign')
        # 签名确保安全性
        result = alipay.verify(data, sign)
        # 订单号
        out_trade_no = data.get('out_trade_no')
        # 订单状态
        trade_status = data.get("trade_status")
        # 异步回调，签名sign校验通过，以及订单状态成功或完成，才能确定支付宝支付成功了
        if result and trade_status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            # print(1111111111111)
            models.Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1)
            logger.critical('订单：%s - %s - 支付成功' % (out_trade_no, trade_status))
            return Response('success')
        return Response('failed')
