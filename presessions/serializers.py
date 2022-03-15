from rest_framework import serializers

from .models import Presession

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
            'get_absolute_url'
        )


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