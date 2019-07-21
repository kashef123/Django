from django.contrib import admin
from django.urls import path
from . import views, model_set, api, analyz, add_disease
from django.views.decorators.csrf import csrf_exempt

admin.autodiscover()

app_name = 'MyClassifier'
urlpatterns = [

    path('', views.index, name='main'),
    path('admin', views.index, name='main'),
    path('predict/', views.ConstDetectDiseases, name='predict'),
    path('signup/', views.signup, name='signup'),
    path('history/', views.history, name='history'),
    path('CheckUser/', views.CheckUser, name='CheckUser'),
    path('goToSignUp/', views.goToSignUp, name='goToSignUp'),
    path('test/', views.test, name='test'),
    path('SignOut/', views.SignOut, name='SignOut'),
    path('MyProfile/', views.MyProfile, name='MyProfile'),
    path('upload/', views.uploadPic, name='uploadPic'),
    path('setModel/', model_set.setModel, name='setModel'),
    path('general/', views.ConstDetectPlant, name='general_det'),
    path('construct/', views.construct, name='construct'),
    path('comment/', views.comment, name='comment'),
    path('API/', csrf_exempt(api.requestAPI), name='API'),
    path('signupapi/', csrf_exempt(api.signupapi), name='signupapi'),
    path('analysisapi/', csrf_exempt(api.analysisapi), name='analysisapi'),

 

    path('analyze/', analyz.get_data, name='Analyze'),

    path('analyze_plant/', analyz.get_plant_data, name='analyze_plant'),

    

    path('addDisease/', add_disease.addDeisease, name='addDisease'),
    path('add/', add_disease.add, name='add'),


    path('earlyblight/', add_disease.earlyblight, name='earlyblight'),
    
    path('lateblight/', add_disease.lateblight, name='lateblight'),
     

    
     
]
