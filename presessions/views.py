from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from presessions.models import Presession
from problems.models import Problem
from users.models import UserInfo
from django.contrib.auth.models import User

from datetime import datetime

from presessions.serializers import PresessionSerializer, PostNewPresessionSerializer

# Create your views here.
# GET All Presessions
class AllPresessions(APIView):
    def get(self, request, format=None):
        presessions = Presession.objects.all()
        serializer = PresessionSerializer(presessions, many=True)
        return Response(serializer.data)

# POST New Presession
class PostNewPresession(APIView):
    def post(self, request, format=None):
        # Get the User and Check if the user status - Busy and then reject
        user = User.objects.get(id=request.data['user'])
        userinfo = UserInfo.objects.filter(user=user)[0]
        
        if (userinfo.is_busy == True):
            return Response({'message': "Sorry, you have already picked a problem. Please solve it first.", 'status':400})
        
        # Get the Problem
        problem = Problem.objects.get(id=request.data['problem'])
        
        # If the problem poster is the same as the user - picker, then reject
        poster = problem.user
        if (poster == user):
            return Response({'message': 'You cannot pick your own problem.', 'status':400})
        
        # Limit the User do not submit repeatedly.
        if (Presession.objects.filter(user=user, problem=problem).exists()):
            return Response({'message': 'Please do not submit repeatedly.', 'status':400})
        
        # Get the Motivation
        motivation = request.data['motivation']
        # Intialize the Result - 0 = Pending
        result = 0
        # Initialize the Reason - Waiting for the Decision
        reason = "Waiting for the decision."
        # Initialize the Date Posted
        date_posted = datetime.now()
        # Initialize the Date Result
        date_result = None
        # Create the Presession
        presession = Presession(
            user=user,
            problem=problem,
            motivation=motivation,
            result=result,
            reason=reason,
            date_posted=date_posted,
            date_result=date_result
        )
        # Save the Presession
        presession.save()
        # Return the Presession
        return Response({'presession': PostNewPresessionSerializer(presession).data, 'status': 201})