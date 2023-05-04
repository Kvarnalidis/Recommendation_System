from django.db import models

# Create your models here.

class Museums(models.Model):
	Name 	 = models.CharField(max_length=120)
	Image 	 = models.ImageField(upload_to='images/')
	Location = models.TextField(blank=True,default=False)
	description = models.TextField(blank=True,default=False)
	price	 = models.IntegerField(default=0)
	theme 	 = models.IntegerField(default=0)
	discountAvailability = models.IntegerField(default=0)	
	pointX	 = models.IntegerField(default=0)
	pointY	 = models.IntegerField(default=0)