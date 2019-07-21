from django.shortcuts import render, get_object_or_404
from MyClassifier.models import USER, PICTURES
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from MyClassifier.forms import PicForm
from MyClassifier import model_v2, plantDetect
import os
from django.http import Http404
from io import StringIO
from PIL import Image
from django.http import JsonResponse
import json
import datetime



def requestAPI(request):
    path = request.POST.get("pathimage")
    plant = request.POST.get("plant")
    uname = request.POST.get("username")
    
    flowers, pred = model_v2.apiresult(path, 0, plant, uname)
    


    return JsonResponse({'flowers': flowers,
                         'pred': pred})

def signupapi(request):

    
    

    user_name = request.POST.get('username')
    email = request.POST.get('email')
    
    
    q = " "
    flag = True
    try:
         if( USER.objects.get(username=user_name)):
             flag = False
             q = q + "Not_valid_username  "
    except USER.DoesNotExist:
        pass

    try:
         if( USER.objects.get(email=email)):
             flag = False
             q = q + "Not_valid_email  "
    except USER.DoesNotExist:
        pass
        
    
    if flag:
        q = "True"
        user = USER(

        username=user_name,
        firstname='firstname',
        lastname='lastname',
        password=request.POST.get('password'),
        email=email,
        mobilenumber= '0',
        country=" ",
        city=" ",
        region=" ",
        usertype="1",
        
        
    )
        user.save()
        

    return JsonResponse({'Result': q})




def analysisapi(request):

    user_name = request.POST.get('username')
    plant_name = request.POST.get('plantname')
    date = request.POST.get('date')
    print(user_name, plant_name , date ) 

    if date == "Last Day":
        no_of_days = 1
    elif date == "Last 15 Days":
        no_of_days = 15
    elif date == "Last 1 Month":
        no_of_days = 30
    elif date == "Last 3 Months":
        no_of_days = 90
    elif date == "Last 6 Months":
        no_of_days = 180
    elif date == "Last Year":
        no_of_days = 365
    elif date == "All Times":
        no_of_days = 0
    else:
        pass


    



    try:
        
        if ( USER.objects.get(username=user_name)):
            
            user =  USER.objects.get(username=user_name)
            q = PICTURES.objects.filter(User=user.id)
            title = ""


            if plant_name != None:  
                q = q.filter(pic_plant= plant_name)
                title = title +  plant_name

            else:
                pass

            if date != None:
                enddate  = datetime.datetime.today()
                startdate = enddate - datetime.timedelta(days=no_of_days)
                q = q.filter(pic_date__range=[startdate, enddate])
            
                title = title + date
            
            else:
                pass
            
            new_plant_data = None
            new_plant_data = {'none': 0}
            for record in q:
                disease_name = str(record.pic_pred_names[0])
            
                if not new_plant_data:
                    new_plant_data[disease_name] = 1
                else:
                    
                    if disease_name not in new_plant_data:
                        new_plant_data[disease_name] = 1
                    elif disease_name in new_plant_data:
                        new_plant_data[ disease_name ] += 1
                    else:
                        pass
                    
            del new_plant_data['none']

            string_result = ''

            for i in new_plant_data:
                string_result = string_result + i +":" + str(new_plant_data[i]) + ","

      



             
    except USER.DoesNotExist:

        string_result = "Not_valid_username"


    


    
    return JsonResponse({'Result': string_result})
