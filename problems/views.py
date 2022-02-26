from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Problem, User
from .serializers import ProblemSerializer
# Create your views here.

class LatestProblemsList(APIView):
    def get(self, request, format=None):
        problems = Problem.objects.all()[:10]
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)
    
class ProblemDetail(APIView):
    def get_object(self, tag_slug, problem_slug):
        try:
            return Problem.objects.filter(tag__slug=tag_slug).get(slug=problem_slug)
        except Problem.DoesNotExist:
            raise Http404
    
    def get(self, request, tag_slug, problem_slug, format=None):
        problem = self.get_object(tag_slug, problem_slug)
        serializer = ProblemSerializer(problem)
        return Response(serializer.data)