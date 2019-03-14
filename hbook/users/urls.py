# The heck
from django.conf.urls import url, include
from knox import views as knox_views
from rest_framework.routers import SimpleRouter, DefaultRouter
from hbook.users.views import LoginGoogleView, User2ViewSet, UserViewSet


router = DefaultRouter()
router.register('user', UserViewSet)
router.register('user2', User2ViewSet)
#router.rgister('googlelogin', LoginGoogleView, base_name='googlelogin')

urlpatterns = [
    url(r'^googlelogin/', LoginGoogleView.as_view()),
    url(r'auth/', include(router.urls)),
    url(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    url(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]