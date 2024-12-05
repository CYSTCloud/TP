from django.db import models

# Create your models here.
class Translation(models.Model):
    
    source_language = models.CharField(max_length=200)
    source_text = models.TextField(default=None)
    target_language = models.CharField(max_length=200)
    target_text = models.TextField(default=None)
    creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.source_language}-{self.source_text}-{self.target_language}-{self.target_text}"