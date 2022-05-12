from rest_framework.views import APIView
from rest_framework.response import Response

from solutions.models import Solution
from problems.models import Problem
from presessions.models import Presession

from solutions.serializers import SolutionSerializer, UpdateSolutionSerializer

# Create your views here.
class GetSolutionsByPickerId(APIView):
    def get(self, request, picker_id):
        solutions = Solution.objects.filter(presession__user_id=picker_id)
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)
    
    
class GetSolutionByProblemId(APIView):
    def get(self, request, problem_id):
        problem = Problem.objects.get(id=problem_id)
        presessions = Presession.objects.filter(problem=problem)
        
        # Condition 1 - Check whether it has been accepted by FlyMeCrods
        accepted_presessions = []
        for presession in presessions:
            if (presession.result == 1):
                accepted_presessions.append(presession)
        
        if (len(accepted_presessions) == 0):
            return Response({"message": "No accepted presessions"})
        
        # Get accepted presessions' solutions
        solutions = []
        for presession in accepted_presessions:
            solutions.append(Solution.objects.get(presession=presession))
            
        # Condition 2 - Check which one is in status -> The only condition is Max ID
        ids = []
        for solution in solutions:
            ids.append(solution.id)
        solution_id = max(ids)
        solution = Solution.objects.filter(id=solution_id)[0]
        
        return Response(SolutionSerializer(solution).data)
    
class GetSolutionById(APIView):
    def get(self, request, solution_id):
        solution = Solution.objects.get(id=solution_id)
        serializer = SolutionSerializer(solution)
        return Response(serializer.data)
    
    
class UpdateSolution(APIView):
    def put(self, request, solution_id):
        solution = Solution.objects.filter(id = solution_id)[0]
        
        text_solution = request.data['text_solution']
        file_solution = request.data['file_solution']
        notice = request.data['notice']
        
        # Check whether there is a file in the database
        if (file_solution == 'null' and solution.file_solution == ''):
            file_solution = None
        if (file_solution == 'null' and solution.file_solution != ''):
            file_solution = solution.file_solution


        formData = {
            'text_solution': text_solution,
            'file_solution': file_solution,
            'notice': notice,
        }
        serializer = UpdateSolutionSerializer(solution, data=formData)

        if serializer.is_valid():
            serializer.save()

            # Update the solution_result to 1 = 'Submitted'
            solution.solution_result = 1
            solution.save()

            return Response({'solution': serializer.data, 'status': 201})
        else:
            return Response({'errors': serializer.errors, 'status': 400})
        
# Get All Solutions
class GetAllSolutions(APIView):
    def get(self, request):
        solutions = Solution.objects.all()
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)