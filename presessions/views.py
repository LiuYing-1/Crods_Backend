from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from presessions.models import Presession
from problems.models import Problem
from users.models import UserInfo
from solutions.models import Solution
from django.contrib.auth.models import User

from datetime import datetime

from presessions.serializers import PresessionSerializer, PostNewPresessionSerializer, UpdatePresessionSerializer

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
            # Respond the User if he has sent the request before
            if (Presession.objects.filter(user=user, problem=problem)[0].result == 1):
                return Response({'message': 'Your request has already been accepted.', 'status':400})
            if (Presession.objects.filter(user=user, problem=problem)[0].result == 2):
                return Response({'message': 'Your request has already been rejected.', 'status':400})
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

class GetPresessionByID(APIView):
    def get(self, request, presession_id, format=None):
        presession = Presession.objects.get(id=presession_id)
        serializer = PresessionSerializer(presession)
        return Response(serializer.data)
    
    
class UpdatePresession(APIView):
    def put(self, request, presession_id, format=None):
        presession = Presession.objects.get(id=presession_id)
        
        # Update the Result
        presession.result = request.data['result']
        # Get the Reason
        reason = request.data['reason']
        
        # Limit the Picker do not pick problem more than one.
        pickerinfo = UserInfo.objects.filter(user=presession.user)[0]
        if (pickerinfo.is_busy == True and  presession.result == 1):
            return Response({'message': "Sorry, this user has already picked a problem currently.", 'status':400})
        else:
            # Update the default reason
            if (reason == "Waiting for the decision."):
                if (presession.result == 1):
                    reason = "Congratulations, your request has been accepted."
                else:
                    reason = "Sorry, your request has been rejected."
            # Update the Reason
            presession.reason = reason
            presession.date_result = datetime.now()
            
            data = {
                'id': presession.id,
                'result': presession.result,
                'reason': presession.reason,
                'date_result': presession.date_result
            }
            
            serializer = UpdatePresessionSerializer(presession, data=data)
            if (serializer.is_valid()):
                serializer.save()
                
                # Close the Audit Process
                if (presession.result == 1):
                    # Update the User Status to Busy
                    pickerinfo = UserInfo.objects.filter(user=presession.user)[0]
                    pickerinfo.is_busy = True
                    pickerinfo.picks_num += 1
                    pickerinfo.save()
                    
                    # Fee (temporary stored in the Platform)
                    problem = Problem.objects.get(id=presession.problem.id)
                    poster = User.objects.get(id=problem.user.id)
                    posterinfo = UserInfo.objects.filter(user=poster)[0]
                    posterinfo.balance -= problem.budget
                    posterinfo.save()
                    # Set Problem Status to In - Progress
                    problem.status = 1
                    problem.save()
                    # Reject other Presessions of the same Problem
                    rej_presessions = Presession.objects.filter(problem=presession.problem, result=0)
                    for rej_pres in rej_presessions:
                        rej_pres.result = 2
                        rej_pres.reason = "Sorry, your request has been rejected."
                        rej_pres.date_result = datetime.now()
                        rej_pres.save()
                    
                    solution = Solution(presession=presession)
                    solution.save()
                    
                return Response({'presession': serializer.data, 'status': 201, 'message': 'Updated Successfully.'})
            else:
                return Response({'presession': serializer.errors, 'status': 400})