from django.db import models
import datetime
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class USER(models.Model):
    username = models.CharField(max_length=100, unique=True, null=True)
    firstname = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=200, unique=True, null=True)
    mobilenumber = models.IntegerField(default=100000, blank=True, null=True)
    usertype = models.IntegerField(null=True)
    country = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=20, null=True)
 

class PICTURES(models.Model):
    User = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)
    pic_pred_names = ArrayField(models.CharField(max_length=200), blank=True , null=True)
    pic_pred_props = ArrayField(models.IntegerField(), blank=True, null=True)
    pic_plant = models.TextField(max_length=100,  null=True)
    pic=models.ImageField(upload_to='pictures/Predictions_pictures', blank=True, null=True)
    pic_date=models.DateField(default=datetime.date.today, null=True)
    pic_rate=models.IntegerField(null=True)
    pic_comment=models.TextField(max_length=200, default="no comment", null=True)
    country = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=20, null=True)


class PRODUCT(models.Model):
    description = models.TextField(null=True)
    name = models.TextField(null=True)
    price = models.IntegerField(null = True)

class Disease(models.Model):
    pic = models.ImageField( upload_to='pictures/Diseases_pictures', blank=True, null=True)
    name = models.TextField(null=True)
    scientific_name = models.TextField(null=True)
    plants = ArrayField(models.TextField(), blank=True, null=True)
    diseasetype = models.TextField(null=True)
    nutshell = ArrayField(models.TextField(), blank=True, null=True)
    symptoms = models.TextField(null=True)
    trigger = models.TextField(null=True)
    biological_control = models.TextField(null=True)
    chemicalcontrol = models.TextField(null=True)
    preventivemesures = ArrayField(models.TextField(), blank=True, null=True)
    product =  models.ForeignKey(PRODUCT, on_delete=models.CASCADE, null=True)


class PLANT(models.Model):
    pic = models.ImageField( upload_to='pictures/Plants_pictures', blank=True, null=True)
    name = models.TextField(null=True)
    arname = models.TextField(null=True)
    state = models.TextField(null=True)
    descrption =  models.TextField(null=True)



class DiseasePlant(models.Model):
    PLANT = models.ForeignKey(PLANT, on_delete=models.CASCADE, null=True)
    Disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True)

