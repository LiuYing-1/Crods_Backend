from django.shortcuts import render
from django.http import Http404

from django.contrib.auth.models import User
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserInfo

from .serializers import UserInfoSerializer

# User Register
class Register(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if User.objects.filter(username = username).exists():
            resp = {
                'status': False,
                'data': 'User already exists'
            }
        else:
            user = User.objects.create_user(username = username, password = password)
            token, created = Token.objects.get_or_create(user = user)
            resp = {
                'status': True,
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
            }
        
        return Response(resp)
    

# User Login
class Login(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'status': True,
            'token': token.key,
            'user_id': user.pk,
            'user_name': user.username,
        })
        

# User Information
class UserInfoDetail(APIView):   
    def get_object(self, user_id):
        try:
            return UserInfo.objects.filter(user__id=user_id).get()
        except:
            raise Http404
        
    def get(self, request, user_id, format=None):
        user_info = UserInfo.objects.get(user_id = user_id)
        serializer = UserInfoSerializer(user_info)
        return Response(serializer.data)