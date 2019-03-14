"""
 Url config
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url('admin/', admin.site.urls),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'api/', include('hbook.users.urls'))
]
