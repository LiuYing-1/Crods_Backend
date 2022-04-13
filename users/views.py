from django.http import Http404

from django.contrib.auth.models import User
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserInfo
from problems.models import Problem
from presessions.models import Presession
from solutions.models import Solution
from distributions.models import Distribution

from .serializers import UserInfoSerializer
from presessions.serializers import PresessionSerializer
from problems.serializers import ProblemSerializer
from distributions.serializers import DistributionSerializer

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
            status = 400
            message = 'Please do not use the same email address'
        else:
            # Check whether the email is already in use
            if User.objects.filter(email = request.data.get('email')).exists():
                status = 400
                message = 'Email already in use'
            else:
                user.email = request.data.get('email')
                user.save()
                status = 201
                message = 'Email updated successfully'
        
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
    
class GetEmailAddressByUsername(APIView):
    def get(self, request, username, format=None):
        user = User.objects.get(username = username)
        if (user.email == '' or user.email == None):
            return Response({
                'status': False,
                'email': 'Has not set email address'
            })
        else:
            return Response({
                'status': True,
                'email': user.email
            })

# For Bar Chart Module in User Profile
class GetUserAcceptedSolutionsWithDate(APIView):
    def get(self, request, user_id, format=None):
        user = User.objects.get(id = user_id)
        # Get All the posted and completed problmes
        problems = Problem.objects.filter(user = user, status = 2)
        # Get All the related accepted presessions
        presessions = []
        for problem in problems:
            presessions.append(Presession.objects.get(problem = problem, result = 1))
        solutions = []
        for presession in presessions:
            solution = Solution.objects.get(presession = presession)
            if solution.solution_result == 2:
                solutions.append(solution)
        # Get All the related distributions
        distributions = []
        for solution in solutions:
            distributions.append(Distribution.objects.get(solution = solution))
        serializer = DistributionSerializer(distributions, many=True)
        return Response(serializer.data)
    
# For Pie Chart Module in User Profile
class GetUserRejectedSolutionsWithDate(APIView):
    def get(self, request, user_id, format=None):
        user = User.objects.get(id = user_id)
        # Get All the posted and completed problmes
        problems = Problem.objects.filter(user = user, status = 2)
        # Get All the related accepted presessions
        presessions = []
        for problem in problems:
            presessions.append(Presession.objects.get(problem = problem, result = 1))
        solutions = []
        for presession in presessions:
            solution = Solution.objects.get(presession = presession)
            if solution.solution_result == 3:
                solutions.append(solution)
        # Get All the related distributions
        distributions = []
        for solution in solutions:
            distributions.append(Distribution.objects.get(solution = solution))
        serializer = DistributionSerializer(distributions, many=True)
        return Response(serializer.data)
    
# For Bar Chart Module in User Profile - Picked Module
class GetUserPassedPresessions(APIView):
    def get(self, request, user_id, format=None):
        user = User.objects.get(id = user_id)
        presessions = Presession.objects.filter(user = user, result = 1)
        serializer = PresessionSerializer(presessions, many=True)
            
        return Response(serializer.data)

class GetUserPickedProblems(APIView):
    def get(self, request, user_id, format=None):
        user = User.objects.get(id = user_id)
        presessions = Presession.objects.filter(user = user, result = 1)
        picked_problems = []
        for presession in presessions:
            picked_problems.append(presession.problem)
        serializer = ProblemSerializer(picked_problems, many=True)
        
        return Response(serializer.data)

class GetUserSubmittedSolutionDistributions(APIView):
    def get(self, request, user_id, format=None):
        user = User.objects.get(id = user_id)
        presessions = Presession.objects.filter(user = user, result = 1)
        picked_problems = []
        for presession in presessions:
            picked_problems.append(presession.problem)
        distributions = []
        for picked_problem in picked_problems:
            distributions.append(Distribution.objects.get(problem = picked_problem))
        serializer = DistributionSerializer(distributions, many=True)
        return Response(serializer.data)