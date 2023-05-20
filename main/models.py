from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Application(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)
    date_of_contract = models.DateField()
    inn = models.CharField(max_length=30)
    test_object = models.CharField(max_length=20)
    defined_characteristic = models.CharField(max_length=100)
    amount = models.IntegerField()
    type_of_documentation = models.CharField(max_length=20)


class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
