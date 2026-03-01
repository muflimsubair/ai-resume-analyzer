from django.db import models

class ResumeAnalysis(models.Model):
    name = models.CharField(max_length=100)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.score}%"