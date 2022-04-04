from rest_framework import serializers

from emails.models import Email

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = (
            'id', 
            'name', 
            'receiver_address', 
            'sender_address', 
            'text', 
            'attatchment', 
            'date_sent', 
            'reply',
            'unread',
            
            'get_sender_username',
            'get_receiver_username',
            )