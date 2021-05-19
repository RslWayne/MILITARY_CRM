from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Dossier(models.Model):
    full_name = models.CharField(max_length=200)
    date_birth = models.DateField()
    image = models.ImageField(blank=True,null=True)
    gender = models.CharField(choices=(
        ('M','M'),
        ('W','W')
    ),max_length=50)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='dossier')


    def __str__(self):
        return self.full_name


class Car(models.Model):
    mark = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.DateField()
    number = models.PositiveIntegerField()
    color = models.CharField(choices=(
        ('yellow','yellow'),
        ('black','black'),
        ('red','red'),
        ('blue','blue')
    ),max_length=50)
    type = models.CharField(max_length=200)
    dossier = models.ForeignKey(Dossier,on_delete=models.CASCADE,related_name='cars')


class Education(models.Model):
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    school_name = models.CharField(max_length=200)
    major = models.CharField(max_length=200)
    dossier = models.ForeignKey(Dossier,on_delete=models.CASCADE,related_name='schools')


class Warcraft(models.Model):
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    military_area = models.CharField(max_length=200)
    major = models.CharField(max_length=200)
    start_pose = models.CharField(max_length=200)
    end_pose = models.CharField(max_length=200)
    dossier = models.ForeignKey(Dossier,on_delete=models.CASCADE,related_name='war_crfts')
