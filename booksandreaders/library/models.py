from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    reader = models.ForeignKey(to='Reader', related_name='books', on_delete=models.SET_NULL, null=True)


class Reader(models.Model):
    name = models.CharField(max_length=100)
