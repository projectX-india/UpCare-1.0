from django.forms import ModelForm
from .models import Blogs,Consultation
from django import forms

class BlogsForm(ModelForm):
	class Meta:
		model=Blogs
		fields=['title','description','image']

class ConsultationForm(ModelForm):
	class Meta:
		model=Consultation
		fields=['name','email','phone','symptoms']