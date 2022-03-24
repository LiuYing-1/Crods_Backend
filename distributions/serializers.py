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
            
            'get_problem_id',
            'get_problem_budget',
            'get_solution_id',
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
        )