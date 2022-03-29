from django.shortcuts import render
from django.http import Http404

from django.contrib.auth.models import User
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserInfo

from .serializers import UserInfoSerializer
from problems.serializers import ProblemSerializer

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
            
            userinfo = UserInfo(user = user)
            userinfo.save()
                        
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
    
# User Email Update
class EmailUpdate(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            raise Http404
    
    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        
        if (user.email == request.data.get('email')): 
            status = False
            message = 'Please do not use the same email address'
        else:
            user.email = request.data.get('email')
            user.save()
            status = True
            message = 'Email updated successfully'
            user.save()
        
        return Response({
            'status': status,
            'message': message,
        })

# Collected User Posted Problems
class UserPostedProblems(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            raise Http404
        
    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        problems = user.problems.all()
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)

# Get Users that Ranked Higher
class RankUserInfosByReputation(APIView):
    def get(self, request, format=None):
        user_infos = UserInfo.objects.all().order_by('-reputation')
        serializer = UserInfoSerializer(user_infos, many=True)
        return Response(serializer.data)