from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    category = models.CharField(max_length=100, default="Unknown")
    language = models.CharField(max_length=20, default="en")
    arrival = models.IntegerField(default=2000)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ("name", "author")

    def __str__(self):
        return f"{self.name} - {self.author}"

