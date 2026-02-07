from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    arrival = models.IntegerField()
    link = models.URLField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email
