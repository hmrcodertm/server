"""
Viewset
"""

from rest_framework import viewsets, response
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework.decorators import action
from knox.views import LoginView as KnoxLoginView
from hbook.users.models import User2, User2Serializer, UserSerializer

class User2ViewSet(viewsets.ModelViewSet):
    """Hell to all
    """
    queryset = User2.objects.all()
    serializer_class = User2Serializer

    @action(detail=False)
    def status(self, request):
        print(request.user)
        if(request.user.username==''):
            return response.Response({'status':'notlogged'})
        else:
            u = User2.objects.get(auth=request.user)
            return response.Response({'status':'islogged', 'is_staff':request.user.is_staff, 'id': request.user.id, 'user':User2Serializer(u, context={'request':request}).data})


class UserViewSet(viewsets.ModelViewSet):
    """
    Default user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class UserSerialiazer()
class LoginGoogleView(KnoxLoginView):
    """The Hek
    """
    permission_classes = ()
    authentication_classes = []

    def post(self, request, format=None):
        token = request.POST.get("id_token", '#')
        if token == '#': 
            return response.Response({'token':'Tha fuck was that'})
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "373414904977-n4id010pcju9nb7e8hj992ceph90ag1l.apps.googleusercontent.com")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            userid = idinfo['sub']
            email = idinfo['email']
            # check if user already exist
            user = User.objects.filter(email=email)
            if len(user)==0:
                # user doesn't exist, so create one
                user = User()
                user.username=userid
                user.email = email
                user.save()
                request.user=user
                user2 = User2()
                user2.name = idinfo['name']
                user2.auth = user
                import json
                user2.info = json.dumps(idinfo)
                user2.save()
            else :
                # User exist, 
                request.user=user[0]
            return super(LoginGoogleView, self).post(request, format=None)
            return response.Response({"username":userid, "email":email})
        except ValueError as e:
            print(e)
            return response.Response({"token":'failed'})