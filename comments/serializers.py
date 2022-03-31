from rest_framework import serializers

from comments.models import Comment, Reply

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 
            'user', 
            'problem', 
            'content', 
            'created_at',
            'like',
            'get_username',
        )
        
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = (
            'id', 
            'user', 
            'comment', 
            'content', 
            'created_at',
            'like',
            'get_username',
        )
        
class PostNewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'user',
            'problem',
            'content',
        )


class PostNewReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = (
            'user',
            'comment',
            'content',
        )