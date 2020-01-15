from django.urls import path, re_path, include
from utils.router import router

from . import views

urlpatterns = [
    path('pay/', views.OrderAPIView.as_view()),
    path('pay/success/', views.OrderSuccessAPIView.as_view()),
]


"""支付模块接口分析
1 订单支付链接 接口
    参数：订单名、总价、支付方式、支付人
    响应：支付链接
    逻辑：根据参数，生成订单记录，产生支付链接返回

2 支付成功的异步回调接口
    参数：支付宝异步回调回来的
    响应：成功 success  7个字符，
    逻辑：根据参数，得到订单支付状态，校验订单状态，更新数据库订单信息
"""
