from MyClassifier.models import USER, PICTURES
import torch
import torch.nn as nn
import numpy as np
from torchvision import models
from collections import OrderedDict
from PIL import Image
import urllib.request
import time
import os
from django.core.files import File


label_map = {
    '0': 'Apple scab',
    "1": "Apple Black rot",
    "2": "Apple Cedar apple rust",
    "3": "Apple healthy",
    "4": "Blueberry healthy",
    "5": "Cherry-including sour-Powdery mildew",
    "6": "Cherry-including sour-healthy",
    "7": "Corn-maize-Cercospora leaf spot Gray leaf spot",
    "8": "Corn-maize-Common rust",
    "9": "Corn_(maize) Northern Leaf Blight",
    "10": "Corn_(maize) healthy",
    "11": "Grape Black rot",
    "12": "Grape Esca_(Black_Measles)",
    "13": "Grape Leaf_blight_(Isariopsis_Leaf_Spot)",
    "14": "Grape healthy",
    "15": "Orange Haunglongbing_(Citrus_greening)",
    "16": "Peach Bacterial spot",
    "17": "Peach healthy",
    "18": "Pepper bell Bacterial spot",
    "19": "Pepper bell healthy",
    "20": "Potato Early blight",
    "21": "Potato Late blight",
    "22": "Potato healthy",
    "23": "Raspberry healthy",
    "24": "Soybean healthy",
    "25": "Squash Powdery mildew",
    "26": "Strawberry Leaf scorch",
    "27": "Strawberry healthy",
    "28": "Tomato Bacterial_spot",
    "29": "Tomato Early blight",
    "30": "Tomato Late blight",
    "31": "Tomato Leaf Mold",
    "32": "Tomato Septoria leaf spot",
    "33": "Tomato Spider mites Two-spotted spider mite",
    "34": "Tomato Target Spot",
    "35": "Tomato Yellow Leaf Curl Virus",
    "36": "Tomato mosaic virus",
    "37": "Tomato healthy"
}


def build_model(plant_name):

    list_50 = ["grape", "cherry", "strawberry", "pepper", "peach"]

    if plant_name in list_50:
        return models.resnet50(pretrained=True)
    else:
        return models.resnet152(pretrained=True)


def build_classifier(plant_name):

    plant_classes = {"apple": 4, "potato": 3, "tomato": 10, "corn": 4,
        "grape": 4, "cherry": 2, "strawberry": 2, "pepper": 2,  "peach": 2}

    return nn.Sequential(OrderedDict([
        ('fc1', nn.Linear(2048, 1000)),
        ('relu1', nn.ReLU()),
        ('drop1', nn.Dropout(0.2)),
        ('fc2', nn.Linear(1000, plant_classes[plant_name])),
        ('output', nn.LogSoftmax(dim=1))
    ]))


def load_model(plant_name):
  # C:\Users\akash\DjangoAPI\models\classifier_grape.pth
    path = "models/classifier_"+plant_name+".pth"

    model = torch.load(path, map_location='cpu')

    loaded_model = build_model(plant_name)

    for par in loaded_model.parameters():
        par.requires_grad = False

    loaded_model.class_to_idx = model['class_idx']

    classifier = build_classifier(plant_name)

    loaded_model.fc = classifier
    loaded_model.load_state_dict(model['state_dict'],  strict=False)
    loaded_model.eval()

    return loaded_model


def process_image(image_path, ID):
 
   # Open the image
    
    # server settings
    '''
    file_name = str(ID) + '.jpg'
    img = urllib.request.urlretrieve(image_path, file_name)
    img = Image.open(file_name)
   
   
    '''

   # pc Settings 
    image_path = image_path[1:]
    img = Image.open(image_path)
   

    # Resize
    if img.size[0] > img.size[1]:
        img.thumbnail((10000, 256))
    else:
        img.thumbnail((256, 10000))
    # Crop
    left_margin = (img.width-224)/2
    bottom_margin = (img.height-224)/2
    right_margin = left_margin + 224
    top_margin = bottom_margin + 224
    img = img.crop((left_margin, bottom_margin, right_margin, top_margin))

    
    # Normalize
    img = np.array(img)/255
    mean = np.array([0.485, 0.456, 0.406])  # provided mean
    std = np.array([0.229, 0.224, 0.225])  # provided std
    img = (img - mean)/std

    # Move color channels to first dimension as expected by PyTorch
    img = img.transpose((2, 0, 1))

    return img

def predict(image_path, ID, model, plant_name):
    print("entering image prediction")

    top_k =  {"apple":4, "potato":3, "tomato":4, "corn":4, "grape":4, "cherry":2, "strawberry":2, "pepper":2,  "peach":2 }
    
    # Process image
    img = process_image(image_path, ID)

    # Numpy -> Tensor
    image_tensor = torch.from_numpy(img).type(torch.FloatTensor)

    # Add batch of size 1 to image
    model_input = image_tensor.unsqueeze(0)

    # Probs
    probs = torch.exp(model.forward(model_input))

    # Top probs
    top_probs, top_labs = probs.topk(1)
    top_probs = top_probs.detach().numpy().tolist()[0]
    top_labs = top_labs.detach().numpy().tolist()[0]
    # Convert indices to classes
    idx_to_class = {val: key for key, val in
                    model.class_to_idx.items()}

    # top_labels = [idx_to_class[lab] for lab in top_labs]

    top_flowers = [label_map[idx_to_class[lab]] for lab in top_labs]
    top_probs = [round(i*100, 2) for i in top_probs]

   

    return top_probs,  top_flowers

def results(image_path , ID, plant_name):
    since = time.time()
    model = load_model(plant_name)
    probs, flowers = predict(image_path, ID, model, plant_name)
    print ("prediction leave disease", time.time()-since)
    return (flowers, probs)

def apiresult(image_path, ID, plant_name, uname):
    since = time.time()
    model = load_model(plant_name)
    probs, flowers = predict(image_path, ID, model, plant_name)
    print("prediction leave disease", time.time()-since)

    result = urllib.request.urlretrieve(image_path) # image_url is a URL to an image


    user = USER.objects.get(username=uname)
    c_pic = PICTURES()
    c_pic.User = user
 
    c_pic.pic.save(
    os.path.basename(image_path),
    File(open(result[0], 'rb'))
    )

    c_pic.pic_pred_props = probs
    c_pic.pic_pred_names = flowers
    c_pic.pic_plant = plant_name
    c_pic.save()

    return flowers, probs