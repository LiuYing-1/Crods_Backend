from django.db import models

from presessions.models import Presession
# Create your models here.
class Solution(models.Model):
    presession = models.ForeignKey(Presession, related_name='solution' , on_delete=models.CASCADE)
    text_solution = models.TextField(blank=True, null=True)
    file_solution = models.FileField(upload_to='solutions/', blank=True, null=True)
    # 0 = Pending, 1 = Accepted, 2 = Rejected
    solution_result = models.IntegerField(default=0)
    
    def __str__(self):
        return f'solution {self.id}'
    
    def get_presession(self):
        presession = Presession.objects.filter(id=self.presession.id)[0]
        return presession
    