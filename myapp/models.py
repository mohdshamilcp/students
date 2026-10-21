from django.db import models

# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    gender=models.CharField(max_length=100)
    photo=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    gender=models.CharField(max_length=100)
    photo=models.CharField(max_length=100)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Complaint(models.Model):
    date=models.DateField()
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=500)
    reply=models.CharField(max_length=100)
    Status=models.CharField(max_length=100)
