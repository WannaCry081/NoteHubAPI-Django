from django.db import models 


class Note(models.Model):
    
    title = models.CharField(max_length = 100)
    body = models.TextField(blank = True)

    team = models.ForeignKey("Team", on_delete=models.CASCADE)    
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
    def __str__(self):
        return self.title