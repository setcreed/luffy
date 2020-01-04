from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from .logging import logger

def exception_handler(exc, context):
    # 先给drf处理客户端异常，如果response为None，代表服务端异常，需要自己处理
    response = drf_exception_handler(exc, context)
    detail = '%s - %s -%s' % (context.get('view'), context.get('request').method, exc)
    if not response:   # 服务端错误
        response = Response({
            'detail': detail
        })

    else:
        response.data = {'detail': detail}
    # 核心： 要将response.data.get('detail')信息记录到日志文件中

    logger.error(response.data.get('detail'))

    return response