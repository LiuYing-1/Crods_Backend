from rest_framework import serializers

from .models import Tag, Problem, User

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = (
            'id', 
            'name', 
            'get_username',
            'get_tagname',
            'get_absolute_url',
            'description', 
            'details', 
            'budget', 
            'deadline', 
            'status', 
            'get_image',
            'get_thumbnail',
            'date_posted',
        )
        
class TagSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True)
    
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "problems",
        )

# Serializer to Post New Problem    
class PostNewProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = (
            "tag",
            "user",
            "name",
            "slug",
            "description",
            "details",
            "budget",
            "deadline",
            "image",
        )
        
# Serializer to Update Problem
class UpdateProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = (
            "id",
            "name",
            'tag',
            "slug",
            "description",
            "details",
            "budget",
            "deadline",
        )