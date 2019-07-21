from django.shortcuts import render, get_object_or_404
from MyClassifier.models import USER, PICTURES
import datetime
import matplotlib.pyplot as plt
import os
import json

def check_loggin_status(request):
     
    if request.session.get('logged_in') == None:
        return True
    else:
        return False


plant_list = []


def get_data(request):
    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})


    us_id = request.session.get('ID')
    # geeting records matching the user id

    pic_data = PICTURES.objects.filter(User=us_id)
    
    #  we need to make list of pictures for each plant
  
    for record in pic_data:
        
        if record.pic_plant not in plant_list:
            if record.pic_plant != None:
                plant_list.append(record.pic_plant)
        else:
            pass
    
 

    return render(request, 'MyClassifier/analyz.html', {'list': plant_list })
    

def get_plant_data(request):
    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})

    us_id = request.session.get('ID')
    # geeting records matching the user id
    plant_name = request.POST.get('plant')
    date = request.POST.get('date')
        

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



    q = PICTURES.objects.filter(User=us_id)


    title = ""


    if plant_name != None:  
        q = q.filter(pic_plant= plant_name)
        title = title +  plant_name

    elif date != None:
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
 



    return plt_img(request, new_plant_data, plant_name, date, title)

    
def plt_img(request, data, plant_name, date, title):

    names = None
    values = None
    names = list(data.keys())
    
    values = list(data.values())
    title = title
    print( names, values)
    '''
    plt.bar(range(len(data)),values,tick_label=names)
    plt.title( title )
    plt.savefig('media/pictures/bar.png')
    plt.clf()
    '''
 
    return render(request, 'MyClassifier/show_plt.html', {'names':names, 'values':values, 'title':title, 'list': plant_list} )

