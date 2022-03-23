from dataclasses import fields
from rest_framework import serializers

from solutions.models import Solution

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = (
            'id',
            'presession',
            'text_solution',
            'file_solution',
            'notice',
            'solution_feedback',
            'solution_result',
            
            'get_presession_date',
            'get_problem_name',
            'get_problem_deadline',
            'get_problem_absolute_url',
            'get_username',
        )
        
        
class UpdateSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = (
            'text_solution',
            'file_solution',
            'notice',
        )

