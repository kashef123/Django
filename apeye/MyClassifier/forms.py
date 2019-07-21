#-*- coding: utf-8 -*-
from django import forms

class PicForm(forms.Form):

   picture = forms.ImageField()
