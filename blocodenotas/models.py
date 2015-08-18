from django.db import models
from django.utils import timezone


# Create your models here.
class Nota(models.Model):

    autor = models.ForeignKey('auth.User')
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __unicode__(self):
        return self.titulo
