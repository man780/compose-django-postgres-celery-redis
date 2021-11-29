from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('education.urls')),
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
]
