from django.db import models
from django.contrib.auth.models import User

from problems.models import Problem
# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-like', '-created_at',)
        
    def __str__(self):
        return self.content

    def get_username(self):
        return self.user.username
    

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-like', '-created_at',)
    
    def __str__(self):
        return self.content
    
    def get_username(self):
        return self.user.username