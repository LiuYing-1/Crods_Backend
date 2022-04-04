from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Email(models.Model):
    name = models.CharField(max_length=100)
    receiver_address = models.EmailField(max_length=254)
    sender_address = models.EmailField(max_length=254)
    text = models.TextField()
    attatchment = models.FileField(upload_to='emails/attatchments/', null=True, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    unread = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-date_sent',)
    
    def __str__(self):
        return self.name
    
    def get_sender_username(self):
        sender = User.objects.get(email=self.sender_address)
        return sender.username
    
    def get_receiver_username(self):
        receiver = User.objects.get(email=self.receiver_address)
        return receiver.username