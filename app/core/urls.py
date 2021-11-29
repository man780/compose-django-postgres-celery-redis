from django.urls import path, include

from .views import AccountViewSet, ChangeBalance
from rest_framework import routers


app_name = 'account'

router = routers.DefaultRouter()
router.register(r'account', AccountViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('change-balance/', ChangeBalance.as_view())
]
