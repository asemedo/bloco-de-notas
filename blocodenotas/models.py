from django.db import models


# Create your models here.
class Notas(models.Model):

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    def __unicode__(self):
        pass
