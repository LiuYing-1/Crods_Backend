from rest_framework.views import APIView
from rest_framework.response import Response

from solutions.models import Solution

from solutions.serializers import SolutionSerializer

# Create your views here.
class GetSolutionsByPickerId(APIView):
    def get(self, request, picker_id):
        solutions = Solution.objects.filter(presession__user_id=picker_id)
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)
    
class GetSolutionById(APIView):
    def get(self, request, solution_id):
        solution = Solution.objects.get(id=solution_id)
        serializer = SolutionSerializer(solution)
        return Response(serializer.data)