from django.db import models

from problems.models import Problem
from solutions.models import Solution

# Create your models here.
class Distribution(models.Model):
    problem = models.ForeignKey(Problem, related_name='distribution', on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, related_name='distribution', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_result = models.DateTimeField(blank=True, null=True)
    # 0 = Pending, 1 = Completed
    result = models.IntegerField(default=0)
    
    # Temp store Rating to Picker
    picker_rating = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-date_posted',)
    
    def __str__(self):
        return f'distribution {self.id}'
    
    def get_problem_name(self):
        return self.problem.name
    
    def get_problem_budget(self):
        return self.problem.budget
    
    def get_poster_name(self):
        return self.problem.user.username
    
    def get_problem_absolute_url(self):
        return self.problem.get_absolute_url()