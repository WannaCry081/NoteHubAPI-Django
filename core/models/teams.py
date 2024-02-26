from django.db import models
from core.utils import code_generater

class Team(models.Model):
    
    profile = models.URLField(blank = True, null = True)
    code = models.CharField(max_length = 8, unique = True,  default = code_generater)
    name = models.CharField(max_length = 20, unique = True)
    description = models.TextField(blank = True)
    
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    members = models.ManyToManyField("User", related_name="user_team", blank = True)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
    def __str__(self):
        return self.name