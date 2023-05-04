from django.db import models

# Create your models here.
 
class Food(models.Model):
	Name 	 = models.CharField(max_length=120)
	Image 	 = models.ImageField(upload_to='images/')
	description = models.TextField(blank=True,default=False)
	Location = models.TextField(blank=True,default=False)
	price	 = models.IntegerField(default=0)
	cuisine	 = models.IntegerField(default=0)
	stars	 = models.IntegerField(default=0)
	pointX	 = models.IntegerField(default=0)
	pointY	 = models.IntegerField(default=0)
