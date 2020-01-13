from rest_framework import pagination


# 基础分页
class PageNumberPagination(pagination.PageNumberPagination):
    # 默认一页显示的条数
    page_size = 2
    # 查询页面的关键字
    page_query_param = 'page'
    # 用户自定义一页显示条数的关键字
    page_size_query_param = 'size'
    # 用户最大可自定义一页显示的条数
    max_page_size = 10


# 偏移分页
class LimitOffsetPagination(pagination.LimitOffsetPagination):
    # 默认一页显示的条数
    default_limit = 2
    # 用户自定义一页显示的条数
    limit_query_param = 'limit'
    # 用户自定义偏移的条数
    offset_query_param = 'offset'
    # 用户最大可自定义一页显示的条数
    max_limit = 10


class CursorPagination(pagination.CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2   # 每页显示2条数据
    ordering = 'id'  # 排序
    page_size_query_param = None
    max_page_size = None