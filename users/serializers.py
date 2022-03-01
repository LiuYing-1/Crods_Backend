from rest_framework import serializers

from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            'user',
            'posts_num',
            'picks_num',
            'is_busy',
            'balance',
            'reputation',
            'get_absolute_url',
        )