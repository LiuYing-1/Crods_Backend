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
            'solution_result',
            'get_presession',
        )