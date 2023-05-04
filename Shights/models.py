from django.db import models

# Create your models here.
class Sights(models.Model):
	Name 	 = models.CharField(max_length=120)
	Image 	 = models.ImageField(upload_to='images/')
	Location = models.TextField(blank=True,default=False)
	description = models.TextField(blank=True,default=False)
	rating	 = models.IntegerField(default=0)
	content	 = models.IntegerField(default=0)
	time 	 = models.IntegerField(default=0)
	pointX	 = models.IntegerField(default=0)
	pointY	 = models.IntegerField(default=0)