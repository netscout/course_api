from django.urls import path
from .views import RouteViewSet

create_update_route = RouteViewSet.as_view({
    'post': 'create',
    'put': 'update',
})

list_route = RouteViewSet.as_view({
    'get': 'list'
})
retrieve_route = RouteViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = [
    path('Route', create_update_route, name="create_update_route"),
    path('Route/', list_route, name="get_route_list"),
    path('Route/<int:pk>', retrieve_route, name="retrieve_route"),
]