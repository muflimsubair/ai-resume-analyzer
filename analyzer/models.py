from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    resume_file = models.FileField(upload_to='resumes/')
    job_description = models.TextField()
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name