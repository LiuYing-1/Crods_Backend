from django.db import models

from problems.models import Problem
from django.contrib.auth.models import User

# Create your models here.
class Presession(models.Model):
    problem = models.ForeignKey(Problem, related_name='presessions', on_delete=models.CASCADE)
    # User - Picker
    user = models.ForeignKey(User, related_name='presessions', on_delete=models.CASCADE)
    # Motivation from the Picker to the Problem
    motivation = models.TextField(blank=False, null=False)
    # Status of the Presession, 0 = Pending, 1 = Accepted, 2 = Rejected
    result = models.IntegerField(default=0)
    # Reason for rejection
    reason = models.TextField(blank=True, null=True)
    # Pub Date of the Presession
    date_posted = models.DateTimeField(auto_now_add=True)
    # Date to Make the Decision
    date_result = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ('-date_posted',)
    
    def __str__(self):
        return f'presession {self.id}'
    
    def get_problem_name(self):
        return self.problem.name
    
    def get_picker_name(self):
        return self.user.username
    
    def get_problem_budget(self):
        return self.problem.budget

    def get_problem_absolute_url(self):
        return self.problem.get_absolute_url()