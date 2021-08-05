from django.urls import path, include

from .views import AccountViewSet, load_data, ChangeBalance
from rest_framework import routers
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

app_name = 'account'

router = routers.DefaultRouter()
router.register(r'account', AccountViewSet)

# account_list = AccountViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# account_detail = AccountViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })
#
# account_highlight = AccountViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])

# urlpatterns = format_suffix_patterns([
#     # path('', api_root),
#     path('accounts/', account_list, name='account-list'),
#     path('account/<uuid>/', account_detail, name='account-detail'),
#     # path('account/<int:pk>/highlight/', account_highlight, name='account-highlight'),
#     # path('users/', user_list, name='user-list'),
#     # path('users/<int:pk>/', user_detail, name='user-detail')
# ])

# from rest_framework.urlpatterns import format_suffix_patterns
#
#
# urlpatterns = [
#     path('account/', views.AccountList.as_view()),
#     path('account/<uuid>/', views.AccountDetail.as_view()),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = [
    path('', include(router.urls)),
    path("change-balance/", ChangeBalance.as_view()),
    path('load_data/', load_data),
]
