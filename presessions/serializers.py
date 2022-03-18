from rest_framework import serializers

from .models import Presession

# Used to Get Presession
class PresessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presession
        fields = (
            'id', 
            'problem',
            'user', 
            'motivation', 
            'result', 
            'reason', 
            'date_posted', 
            'date_result',
            'get_problem_name', 
            'get_picker_name',
            'get_problem_budget',
            'get_problem_absolute_url',
        )

# Used to Post New Presession
class PostNewPresessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presession
        fields = (
            'id', 
            'problem', 
            'user', 
            'motivation', 
            'result', 
            'reason', 
            'date_posted', 
            'date_result',
        )
        
# Admin to Process the Presession
class UpdatePresessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presession
        fields = (
            'id',
            'result',
            'reason',
            'date_result',
        )