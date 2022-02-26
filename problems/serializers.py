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