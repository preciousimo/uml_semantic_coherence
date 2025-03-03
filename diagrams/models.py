from django.db import models

class UseCaseDiagram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='use_case_diagrams/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ClassDiagram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='class_diagrams/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name