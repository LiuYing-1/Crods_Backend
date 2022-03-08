from ast import Return
from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Problem, User, Tag
from users.models import UserInfo
from .serializers import ProblemSerializer, TagSerializer, PostNewProblemSerializer
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
    
class PostNewProblem(APIView):
    def post(self, request, format=None):
        # Get Tag with tag_name
        tag_name = request.data.get('problem_tag')
        tag = Tag.objects.get(name=tag_name)
        
        # Get User with user_id
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        
        # Deal with the name of the problem
        name = request.data.get('problem_name')
        
        tempt = name
        if (' ' in name):
            tempt = name.strip()
        tempt = tempt.lower()
        slug = tempt.replace(' ', '-')

        description = request.data.get('problem_description')
        details = request.data.get('problem_details')
        budget = request.data.get('problem_budget')
        deadline = request.data.get('problem_deadline')
        image = request.data.get('problem_image')
        
        
        serializer = PostNewProblemSerializer(
            data={
                'tag': tag.id,
                'user': user.id, 
                'name': name, 
                'slug': slug, 
                'description': description, 
                'details': details, 
                'budget': budget, 
                'deadline': deadline, 
                'image': image
            })
        
        if serializer.is_valid():
            serializer.save()
            userinfo = UserInfo.objects.filter(user = user)[0]
            userinfo.posts_num += 1
            userinfo.save()
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    
    if query:
        problems = Problem.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)
    else:
        return Response({"problems": []})