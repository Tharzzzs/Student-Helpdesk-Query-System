from django.db import models

# Create your models here.
class Request(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title