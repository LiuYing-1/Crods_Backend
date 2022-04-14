import datetime
from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Problem, User, Tag
from users.models import UserInfo
from .serializers import ProblemSerializer, TagSerializer, PostNewProblemSerializer, UpdateProblemSerializer
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


# Update Problem
class problemUpdate(APIView):
    def get_object(self, problem_id):
        try:
            return Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            raise Http404
        
    def put(self, request, problem_id, format=None):
        problem = self.get_object(problem_id)
          
        problem.name = request.data.get('name')
        
        # Process the Tag of the problem
        newTagName = request.data.get('get_tagname')
        problem.tag = Tag.objects.get(name=newTagName)
        
        # Process the Slug
        tempt = problem.name # Bug 1 => Already Fixed
        if (' ' in problem.name):
            tempt = problem.name.strip()
        tempt = tempt.lower()
        problem.slug = tempt.replace(' ', '-')
        
        # Process the deadline
        problem.deadline = datetime.datetime.strptime(request.data.get('deadline'), "%Y-%m-%d")
        now = datetime.datetime.now()
        
        # Get the rest information
        problem.budget = request.data.get('budget')
        problem.description = request.data.get('description')
        problem.details = request.data.get('details')

        # Condition 1 - Deadline cannot be in the past
        if (problem.deadline < now):
            return Response({'status':400, 'message':'Please Reset the Deadline'})
        
        # Condition 2 - The problem cannot be updated when the status is not 'Unaccepted'
        if (problem.status != 0):
            return Response({'status':400, 'message':'Cannot Update the Problem'})
                    
        
        # Form the data for the serializer
        updatedData = {
            "id": problem.id,
            "name": problem.name,
            "tag": problem.tag.id,
            "slug": problem.slug,
            "description": problem.description,      
            "details": problem.details,
            "budget": problem.budget,
            "deadline": problem.deadline,      
        }                
    
        # Serialize the data
        serializer = UpdateProblemSerializer(problem, data=updatedData)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':200, 'message':'Problem Successfully Updated', 'problem':serializer.data})
        return Response(serializer.errors, status=400)

# Draw Charts for Admin
class GetAllProblems(APIView):
    def get(self, request, format=None):
        problems = Problem.objects.all()
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)


# Search Problems
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    
    if query:
        problems = Problem.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(tag__name__icontains=query))
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)
    else:
        return Response({"problems": []})