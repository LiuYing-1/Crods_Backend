from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    posts_num = models.IntegerField(default=0)
    picks_num = models.IntegerField(default=0)
    is_busy = models.BooleanField(default=False)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    reputation = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return f'/users/{self.user.id}/'