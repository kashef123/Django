from django.shortcuts import render, get_object_or_404
from MyClassifier.models import USER, PICTURES, Disease
import datetime
import matplotlib.pyplot as plt
import os
 

def addDeisease(request):

    list_of_preventive = request.POST.get('disease_preventive_mesures')
    preventive_mesures =  list_of_preventive.splitlines()


    list_of_plants = request.POST.get('disease_plants')
    plants = list_of_plants.splitlines()

    disease_nutshell = request.POST.get('disease_breif')
    breif = disease_nutshell.splitlines()


    new_disease = Disease()

    new_disease.id = request.POST.get('disease_id')
    new_disease.pic = request.FILES['disease_pic']
    new_disease.name = request.POST.get('disease_name')
    new_disease.scientific_name = request.POST.get('disease_scientific_name')
    new_disease.plants = plants
    new_disease.diseasetype = request.POST.get('disease_type')
    new_disease.nutshell = breif
    new_disease.symptoms = request.POST.get('disease_symptoms')
    new_disease.trigger = request.POST.get('disease_trigger')
    new_disease.biologicalcontrol = request.POST.get('disease_biological_control')
    new_disease.chemicalcontrol = request.POST.get('disease_chemical_control')
    new_disease.preventivemesures = preventive_mesures

    new_disease.save()
   
    return render(request, "MyClassifier/addDisease.html")



def add( request ):
    list_of_choices = ["Virus",  "Fungus",  "Bacteria",   "Mite","Insect", "Deficiency"]
    return render(request, "MyClassifier/addDisease.html", {"choices":list_of_choices})


def earlyblight(request):
    return render(request, "MyClassifier/earlyblight.html")

    lateblight


def lateblight(request):
    return render(request, "MyClassifier/lateblight.html")