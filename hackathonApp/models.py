from django.db import models

# Create your models here.

class Estoque(models.Model):
    id = models.AutoField(primary_key=True)
    tecido = models.IntegerField()
    algodao = models.IntegerField()
    fio = models.IntegerField()
    poliester = models.IntegerField()
