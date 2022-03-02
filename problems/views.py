from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Problem, User, Tag
from .serializers import ProblemSerializer, TagSerializer
# Create your views here.

class LatestProblemsList(APIView):
    def get(self, request, format=None):
        problems = Problem.objects.all()[:12]
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
    
class TagDetail(APIView):
    def get_object(self, tag_slug):
        try:
            return Tag.objects.get(slug=tag_slug)
        except Tag.DoesNotExist:
            raise Http404
    
    def get(self, request, tag_slug, format=None):
        tag = self.get_object(tag_slug)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
class ProblemsByStatus(APIView):
    def get_object(self, status):
        try:
            return Problem.objects.filter(status=status)
        except Problem.DoesNotExist:
            raise Http404
    
    def get(self, request, status, format=None):
        problems = self.get_object(status)
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)
    

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    
    if query:
        problems = Problem.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)
    else:
        return Response({"problems": []})