from rest_framework.routers import Route, DynamicRoute, SimpleRouter as DRFSimpleRouter


class SimpleRouter(DRFSimpleRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'put': 'multiply_update',
                'patch': 'multiply_partial_update',
                'delete': 'multiply_destroy'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


router = SimpleRouter()

"""
/users/
'get': 'list',    # 群查
'post': 'create',   # 单增、群增
'put': 'multiply_update',   # 群整改
'patch': 'multiply_partial_update',   # 群局部改
'delete': 'multiply_destroy'    # 群删


/users/(pk)/
'get': 'retrieve',
'put': 'update',
'patch': 'partial_update',
'delete': 'destroy'
"""
