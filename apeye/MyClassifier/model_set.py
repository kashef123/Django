from django.shortcuts import render
from MyClassifier.views import check_loggin_status
from MyClassifier.plantDetect import detect


def setModel(request):
    model_name = request.POST.get('plant_name')
    request.session['model'] = model_name
    if model_name == "general":
        request.session['type'] = 'plant'
    
    return render(request, 'MyClassifier/prediction.html')



