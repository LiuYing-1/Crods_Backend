from rest_framework import serializers

from .models import Distribution

class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = (
            'id', 
            'problem', 
            'solution', 
            'date_posted', 
            'date_result', 
            'result',
            'picker_rating',
            'get_problem_name',
            'get_poster_name',
            'get_problem_budget',
            'get_problem_absolute_url',
        )

class PostNewDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = (
            'problem',
            'solution',
            'date_posted',
            'date_result',
            'result',
            'picker_rating',
        )