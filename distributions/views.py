from decimal import Decimal
from datetime import datetime
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from distributions.models import Distribution
from problems.models import Problem
from solutions.models import Solution
from presessions.models import Presession
from users.models import UserInfo
from django.contrib.auth.models import User

from distributions.serializers import DistributionSerializer, PostNewDistributionSerializer

# Create your views here.
class GetAllDistributions(APIView):
    def get(self, request):
        distributions = Distribution.objects.all()
        serializer = DistributionSerializer(distributions, many=True)
        return Response(serializer.data)
    
# Post New Distribution by Poster
class PostNewDistribution(APIView):
    # Process => {
    #    a1. solution.solution_result <Change>
    #    a2. solution.solution_feedback <Change>
    #    b1. problem.status = 2 <Close the Transaction Session>
    #    c1. Picker IsBusy = False    
    #    d1. Create Distribution
    # }
    def post(self, request, format=None):
        # Get all the information sent from the Frontend - Poster
        problem = Problem.objects.get(id=request.data['problem_id'])
        solution = Solution.objects.filter(id=request.data['solution_id'])[0]
        solution_feedback = request.data['feedback']
        picker_reputation = request.data['rating']
        # Seek the corresponding picker and add the reputation
        picker = User.objects.filter(username=request.data['picker_name'])[0]
        picker_info = UserInfo.objects.filter(user=picker)[0]
        
        # Solution <Result> <Feedback>
        solution.solution_result = request.data['result']
        solution.solution_feedback = solution_feedback
        solution.save()
        # Picker is_busy => Back to UnBusy (False)
        picker_info.is_busy = False
        picker_info.save()
        # Poster - Close the Session
        problem.status = 2
        problem.save()
        
        # Post New Distribution
        date_posted = datetime.now()
        distribution = Distribution(
            problem = problem,
            solution = solution,
            date_posted = date_posted,
            date_result = None,
            result = 0,
            
            picker_rating = picker_reputation,
        )
    
        distribution.save()
        
        return Response({'distribution': PostNewDistributionSerializer(distribution).data, 'status': 201})
    
# Get Distribution by ID
class GetDistributionById(APIView):
    def get(self, request, distribution_id):
        distribution = Distribution.objects.get(id=distribution_id)
        serializer = DistributionSerializer(distribution)
        return Response(serializer.data)
    
# Update Distribution by ID    
class UpdateDistribution(APIView):
    def put(self, request, distribution_id):
        distribution = Distribution.objects.filter(id=distribution_id)[0]
        
        # Priority 1 - What about the Solution hasn't been done or Submitted later ? => If Rejected, money back to Poster (Latest Conclusion)
        # Priority 2 - how to calculate the rating ?
        
        # Check whether the solution is done or not - Check whether it is rejected automatically or mannaually => To the same end (Priority 1)
        # Condition - Text is not empty or not
        solution = Solution.objects.filter(id=distribution.solution.id)[0]    
        # Get Picker    
        presession = Presession.objects.filter(id=solution.presession.id)[0]
        picker = User.objects.filter(username=presession.user.username)[0]
        picker_info = UserInfo.objects.filter(user=picker)[0]
        # Get Poster
        problem = Problem.objects.filter(id=distribution.problem.id)[0]
        poster = User.objects.filter(username=problem.user.username)[0]
        poster_info = UserInfo.objects.filter(user=poster)[0]
        
        # Automatically Rejected OR Manually Rejected
        if (solution.text_solution == None):
            # Refund the Poster => Only Automatically Rejected => 10% of the Budget to the Poster
            poster_info.balance = (problem.budget * Decimal(1.1)) + poster_info.balance
            picker_info.balance = picker_info.balance - (problem.budget * Decimal(0.1))
        if ((solution.solution_result == 3) and solution.text_solution != None):
            # Money Back to Poster
            poster_info.balance += problem.budget
        if (solution.solution_result == 2):
            # Money Sent to Picker
            picker_info.balance += problem.budget
            
        # Align Data to the Model
        distribution.date_result = datetime.now()
        # Only One Result - "Done"
        distribution.result = 1

        # Align the Rating to the Picker (Priority 2) - Accumulated Rating
        picker_info.reputation += distribution.picker_rating
        
        # Save All
        distribution.save()
        picker_info.save()
        poster_info.save()
        
        return Response({'distribution': DistributionSerializer(distribution).data, 'status': 201})