import torch
import torch.nn as nn
import numpy as np
from torchvision import models
from collections import OrderedDict
from PIL import Image
import urllib.request
import time

label_map = {
    '0': 'apple',
    "1": "blueberry",
    "2": "cherry",
    "3": "corn",
    "4": "grape",
    "5": "orange",
    "6": "peach",
    "7": "pepper",
    "8": "potato",
    "9": "rasberry",
    "10": "soybean",
    "11": "squash",
    "12": "strawberry",
    "13": "tomato"
}


def build_model(plant_name):

    list_50 = ["general"]

    if plant_name in list_50:
        return models.resnet50(pretrained=True)
    else:
        return models.resnet152(pretrained=True)


def build_classifier(plant_name):

    plant_classes = {"general": 14}

    return nn.Sequential(OrderedDict([
        ('fc1', nn.Linear(2048, 1000)),
        ('relu1', nn.ReLU()),
        ('drop1', nn.Dropout(0.2)),
        ('fc2', nn.Linear(1000, plant_classes[plant_name])),
        ('output', nn.LogSoftmax(dim=1))
    ]))


def load_model(plant_name):
     
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


def process_image(image_path):
    print("plant detection  entering image processing")
   # Open the image

    # server settings
    '''
    file_name =  str(ID) +'.jpg'
    img = urllib.request.urlretrieve(image_path, file_name)
    img = Image.open(file_name)
    '''

   # pc Settings

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


def predict(image_path, model):
    print("plant detection entering image prediction")

    # Process image
    img = process_image(image_path)

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

    #top_labels = [idx_to_class[lab] for lab in top_labs]

    top_flowers = [label_map[idx_to_class[lab]] for lab in top_labs]
    top_probs = [round(i*100, 2) for i in top_probs]

    return top_probs,  top_flowers


def detect(image_path):
    since = time.time()
    model = load_model("general")
    prob, plant = predict(image_path, model)
    print('plant is', plant)
    print('time for plant detection', time.time()-since )
    return (plant, prob)
