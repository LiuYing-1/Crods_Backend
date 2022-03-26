from django.db import models

from presessions.models import Presession
# Create your models here.
class Solution(models.Model):
    presession = models.ForeignKey(Presession, related_name='solution' , on_delete=models.CASCADE)
    text_solution = models.TextField(blank=True, null=True)
    file_solution = models.FileField(upload_to='solutions/', blank=True, null=True)
    notice = models.TextField(blank=True, null=True)
    solution_feedback = models.TextField(blank=True, null=True)
    # 0 = Pending, 1 = Submitted, 2 = Accepted, 3 = Rejected
    solution_result = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['presession']
    
    def __str__(self):
        return f'solution {self.id}'
    
    def get_presession_date(self):
        return self.presession.date_result
    
    def get_problem_name(self):
        return self.presession.problem.name
    
    def get_problem_deadline(self):
        return self.presession.problem.deadline
    
    def get_problem_absolute_url(self):
        return self.presession.problem.get_absolute_url()
    
    def get_username(self):
        return self.presession.user.username
    