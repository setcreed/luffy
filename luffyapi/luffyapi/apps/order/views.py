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


class OrderSuccessAPIView(APIView):
    pass
