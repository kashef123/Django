from django.shortcuts import render, get_object_or_404
from MyClassifier.models import USER, PICTURES, Disease, PLANT
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from MyClassifier.forms import PicForm
from MyClassifier import model_v2, plantDetect
import os
from django.http import Http404
from io import StringIO
from PIL import Image
 


def check_loggin_status(request):
    print(request.session.get('logged_in'))
    if request.session.get('logged_in') == None:
        return True
    else:
        return False

def plantchoose( request ):
        plants = PLANT.objects.all()
        return render(request, 'MyClassifier/plant_chooser.html', {'plants': plants})


def signup(request):

    user_name = request.POST.get('UserName')
    email = request.POST.get('Email')
    mobile_num = request.POST.get('phone')

    # check if the user used before
    try:
        if USER.objects.get(username=user_name):
            return render(request, 'MyClassifier/SignUp.html', {'error_user': " user not available"})
    except USER.DoesNotExist:
        pass

    # check if the email used before
    try:
        if USER.objects.get(email=email):
            return render(request, 'MyClassifier/SignUp.html', {'error_email': " this email used before"})
    except USER.DoesNotExist:
        pass

    # check if the phone used before
    try:
        if USER.objects.get(mobilenumber=mobile_num):
            return render(request, 'MyClassifier/SignUp.html', {'error_email': " this phone is not valid"})
    except USER.DoesNotExist:
        pass

    user = USER(

        username=user_name,
        firstname=request.POST.get('FirstName'),
        lastname=request.POST.get('LastName'),
        password=request.POST.get('PassWord'),
        email=email,
        mobilenumber=mobile_num,
        country=request.POST.get('country'),
        city=request.POST.get('city'),
        region=request.POST.get('region'),
        usertype=request.POST.get('usertype'),
        
    )
    user.save()

    request.session['logged_in'] = True
    request.session['ID'] = user.id

     

    return render(request, 'MyClassifier/prediction.html')



def index(request):

    if check_loggin_status(request):
       return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})
    else: 
        return plantchoose( request )


def save_pic(request):
    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})

    if request.method == "POST":
        MyPic = PicForm(request.POST, request.FILES)
        if MyPic.is_valid():

            user = USER.objects.get(id=request.session.get('ID'))
            c_pic = PICTURES()
            c_pic.User = user
            c_pic.pic = request.FILES['picture']
            c_pic.country = user.country
            c_pic.city = user.city
            c_pic.region = user.region
            c_pic.save()  
            
            print('picture saved while saving picture ')
            request.session['pictureID'] = c_pic.id

            
    else:
        MyPic = PICTURES()
    
    return (c_pic)


def DetectDiseases(request,  c_pic ):
    path = c_pic.pic.url    
    print("path", path)
    ID = request.session.get('ID')


    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})


    # get the predictions for image
    plant_name = request.session['model']
    names, probs = model_v2.results(path, ID, plant_name)

    # save in the database the probs and names for the pic

    c_pic.pic_pred_props = probs
    c_pic.pic_pred_names = names
    c_pic.pic_plant = plant_name
    # save the pic in the database

    c_pic.save()


    disease = Disease.objects.filter()
    dictionry = {'url': c_pic.pic.url,
                 "probs": probs,
                 "names": names,
                  
                 }

    return render(request, 'MyClassifier/result.html', dictionry)


def DetectPlant(request,  path):


    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})

    name, prob = plantDetect.detect(path)
    request.session['model'] = name[0]
    return 


def ConstDetectDiseases(request):
    c_pic = save_pic(request)
    return DetectDiseases (request,  c_pic )



def ConstDetectPlant(request):
    c_pic = save_pic(request)
    path = c_pic.pic.url
    print("path of picture", path)
    DetectPlant (request,  path)
    return  DetectDiseases (request,  c_pic )


def construct(request):
    if request.session.get('type') == 'plant':

        return ConstDetectPlant(request)
    else:
        return ConstDetectDiseases(request)

def history(request):
    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})

     # geting user user_name
    us_id = request.session.get('ID')
    # geeting records matching the user id

    query = PICTURES.objects.filter(User=us_id)
    # exclude pictures without prediction and precentages
    query = query.exclude(pic_pred_names=None)
    query = query.exclude(pic_pred_props=None)

    return render(request, 'MyClassifier/history.html', {'query': query})


def CheckUser(request):

    user_name = request.POST.get('UserName')
    password = request.POST.get('Password')
    try:
        user = USER.objects.get(username=user_name)
    except USER.DoesNotExist:
        return render(request, 'MyClassifier/index.html', {'error': " not registered USER"})
 
    if password == user.password:

        request.session['logged_in'] = True
        request.session['ID'] = user.id

        return plantchoose( request )
    else:
        return render(request, 'MyClassifier/index.html', {'error': " wrong  password"})


def goToSignUp(request):
    return render(request, "MyClassifier/SignUp.html")


def test(request):
    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})
    return plantchoose( request )


def SignOut(request):

    try:
        del request.session['ID']
        del request.session['logged_in']
    except:
        pass

    return render(request, 'MyClassifier/index.html')


def MyProfile(request):
    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})

    user = USER.objects.get(id=request.session.get('ID'))

    informtion = {'uname': user.username,
                  'fname': user.firstname,
                  'pass': user.password,
                  'lname': user.lastname,
                  'email': user.email,
                  'mnum': user.mobilenumber}

    return render(request, 'MyClassifier/myprofile.html', informtion)


def uploadPic(request):
    if check_loggin_status(request):
        return render(request, 'MyClassifier/index.html', {'error': "Sign in first"})
    return render(request, 'MyClassifier/upload.html')


def comment(request):
    print('i am here in comment')
    c_pic_id =  request.session.get('pictureID')
    
    print("pic id is ", c_pic_id)
    c_pic = PICTURES.objects.get(id=c_pic_id)
    c_pic.pic_comment = request.POST.get('comment')
    print("pic comment is ", c_pic.pic_comment)
    print("user id ", c_pic.User )
    c_pic.save()
    return plantchoose( request )



    