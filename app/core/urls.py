from django.urls import path, include

from .views import AccountViewSet, ChangeBalance
from rest_framework import routers
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'account'

router = routers.DefaultRouter()
router.register(r'account', AccountViewSet)
# router.register(r'account', AccountViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('change-balance/', ChangeBalance.as_view())
]
