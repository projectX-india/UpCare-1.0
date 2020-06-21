from django.db import models
from django.contrib.auth.models import User

class Blogs(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='blogs/images/',default='image_1.jpg')
	user=models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class News(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='news/images/')

	def __str__(self):
		return self.title

class Consultation(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField(max_length=254)
	phone = models.CharField(max_length=13)
	symptoms = models.TextField()

	def __str__(self):
		return self.name

class NeurologyNews(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='NeurologyNews/images/')

	def __str__(self):
		return self.title

class SurgicalNews(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='SurgicalNews/images/')

	def __str__(self):
		return self.title

class DentalNews(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='DentalNews/images/')

	def __str__(self):
		return self.title

class OphthalmologyNews(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='OphthalmologyNews/images/')

	def __str__(self):
		return self.title

class CardiologyNews(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='CardiologyNews/images/')

	def __str__(self):
		return self.title

class DietNews(models.Model):
	title=models.CharField(max_length=100)
	date= models.DateField(auto_now_add=True)
	description = models.TextField()
	image=models.ImageField(upload_to='DietNews/images/')

	def __str__(self):
		return self.title