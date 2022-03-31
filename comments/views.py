from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from problems.models import Problem
from comments.models import Comment, Reply
from comments.serializers import CommentSerializer, PostNewReplySerializer, ReplySerializer, PostNewCommentSerializer
# Create your views here.
class GetCommentsByProblemId(APIView):
    def get(self, request, problem_id, format=None):
        comments = Comment.objects.filter(problem_id=problem_id)
        serializer = CommentSerializer(comments, many=True)
        
        return Response(serializer.data)
    
class PostNewComment(APIView):
    def post(self, request, format=None):
        serializer = PostNewCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class GetRepliesByCommentId(APIView):
    def get(self, request, comment_id, format=None):
        replies = Reply.objects.filter(comment_id=comment_id)
        serializer = ReplySerializer(replies, many=True)
        
        return Response(serializer.data)
    
class PostNewReply(APIView):
    def post(self, request, format=None):
        serializer = PostNewReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class GetCommentById(APIView):
    def get(self, request, comment_id, format=None):
        comment = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(comment)
        
        return Response(serializer.data)


class GetReplyById(APIView):
    def get(self, request, reply_id, format=None):
        reply = Reply.objects.get(id=reply_id)
        serializer = ReplySerializer(reply)
        
        return Response(serializer.data)

class LikeOperation(APIView):
    def put(self, request, format=None):
        comment_id = request.data['comment']
        reply_id = request.data['reply']
        
        if reply_id != 0:
            reply = Reply.objects.get(id=reply_id)
            reply.like += 1
            reply.save()    
        
        if comment_id != 0:
            comment = Comment.objects.get(id=comment_id)
            comment.like += 1
            comment.save()
        
        return Response(request.data)