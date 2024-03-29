from io import BytesIO
from PIL import Image

from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    
class Problem(models.Model):
    tag = models.ForeignKey(Tag, related_name='problems', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='problems', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=False, null=False)
    details = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ('-date_posted',)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.tag.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return settings.BACKEND_PORTAL + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return settings.BACKEND_PORTAL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return settings.BACKEND_PORTAL + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)
        
        return thumbnail
    
    def get_username(self):
        username = self.user.username
        return username
    
    def get_tagname(self):
        tagname = self.tag.name
        return tagname