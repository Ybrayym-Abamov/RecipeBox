from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length = 30)
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    favorites = models.ManyToManyField(
        'RecipeItem',
        related_name='favorites',
        blank=True
    )

    def __str__(self):
        return self.name

class RecipeItem(models.Model):
    title = models.CharField(max_length = 20)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    description = models.TextField()
    time_required = models.CharField(max_length = 20)
    instructions = models.TextField()


    def __str__(self):
        return f"{self.title} - {self.author}"