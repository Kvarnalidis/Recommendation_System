from django.shortcuts import render,redirect
from .forms import FoodChoiceForm

#imports for algorithm 
from Food.models import Food
import math


# Create your views here.
#basic view for the page
def food_choice_view(request):
	#global price,dist,cuisine,stars,priority0,priority1,priority2


	next =request.GET.get('next')
	form =FoodChoiceForm(request.POST)
	if form.is_valid():
		price =form.cleaned_data['price_choice']
		dist = form.cleaned_data['distance_choice']
		cuisine =form.cleaned_data['cuisine_choice']
		stars= form.cleaned_data['star_choice']
		priority1=form.cleaned_data['priority_choice1']
		priority2=form.cleaned_data['priority_choice2']
		priority3=form.cleaned_data['priority_choice3']
		[position,F,score] = algorithm(price,dist,cuisine,stars,priority1,priority2,priority3)
		print(position)
		[priceDB,cuisineDB,starsDB] = getDBvalues(position,F)
		context1={
			'name':"Restaurant Name: "+F[position].Name,
			'image':F[position].Image,
			'description':"Description: "+F[position].description,
			'location':"Address: "+F[position].Location,
			'score':"Penalty score: "+str(score),
			'input1':"Price range: "+priceDB,
			'input2':"Restaurant cuisine: "+cuisineDB,
			'input3':"Michelin stars: "+starsDB
		}
		if next:
			return redirect(next)
		return render(request,"resaults.html",context1)

	context={
		'form':form
	}
	return render(request,"food.html",context)	


#get the appropriate info from db in strings
def getDBvalues(position,F):
	if(F[position].price==0):
		priceDB="Cheap"
	elif(F[position].price==1):
		priceDB="Average"
	else:
		priceDB="Expensive"

	if(F[position].cuisine==0):
		cuisineDB="Italian"
	elif(F[position].cuisine==1):
		cuisineDB="Fast Food"
	elif(F[position].cuisine==2):
		cuisineDB="Greek"
	elif(F[position].cuisine==3):
		cuisineDB="Lebanese"
	else:
		cuisineDB="Chinese"

	if(F[position].stars==0):
		starsDB="1 star"
	elif(F[position].stars==1):
		starsDB="2 stars"
	else:
		starsDB="3 stars"
	return [priceDB,cuisineDB,starsDB]

#calculate the corresponding values for comparison with the database
def calculateChoiceValues(uPrice, uCuisine, uStars, uDistance):
	#price
	if(uPrice=="c"):
		uPriceValue=0
	elif(uPrice=="a"):
		uPriceValue=1
	elif(uPrice=="0"):
		uPriceValue=-10
	else:
		uPriceValue=2
	
	#stars
	if(uStars=="one"):
		uStarsValue=0
	elif(uStars=="two"):
		uStarsValue=1
	elif(uStars=="three"):
		uStarsValue=2
	else:
		uStarsValue=-10
	
	#distance
	if(uDistance=="close"):
		uDistanceValue=0
	elif(uDistance=="avg"):
		uDistanceValue=1
	elif(uDistance=="0"):
		uDistanceValue=-10
	else:
		uDistanceValue=2
	
	#cuisine
	if(uCuisine=="i"):
		uCuisineValue=0
	elif(uCuisine=="f"):
		uCuisineValue=1
	elif(uCuisine=="g"):
		uCuisineValue=2
	elif(uCuisine=="l"):
		uCuisineValue=3
	elif(uCuisine=="0"):
		uCuisineValue=-10
	else:
		uCuisineValue=4
	return [uPriceValue,uStarsValue,uDistanceValue,uCuisineValue]


#calculate weights according to the priorities
def calculateWeights(uPriority1, uPriority2, uPriority3, priceW, cuisineW, starsW, distanceW):
	if(uPriority1=="price"):
		priceW=priceW+1
	elif(uPriority1=="cuisine"):
		cuisineW=cuisineW+1
	elif(uPriority1=="stars"):
		starsW=starsW+1
	elif(uPriority1=="dist"):
		distanceW=distanceW+1

	if(uPriority2=="price"):
		priceW=priceW+0.6
	elif(uPriority2=="cuisine"):
		cuisineW=cuisineW+0.6
	elif(uPriority2=="stars"):
		starsW=starsW+0.6
	elif(uPriority2=="dist"):
		distanceW=distanceW+0.6
		
	if(uPriority3=="price"):
		priceW=priceW+0.2
	elif(uPriority3=="cuisine"):
		cuisineW=cuisineW+0.2
	elif(uPriority3=="stars"):
		starsW=starsW+0.2
	elif(uPriority3=="dist"):
		distanceW=distanceW+0.2
	return [priceW, cuisineW, starsW, distanceW]



def algorithm(priceInput, distInput, cuisineInput, starsInput, priority1Input, priority2Input, priority3Input):
	priceW=1.0
	cuisineW=1.0
	distanceW=1.0
	starsW=1.0
	score=[0.0]

	F=Food.objects.all()
	size=F.count()

	for i in range(1,size):
		score.append(0)

	uPosX=0
	uPosY=0
	uPrice=priceInput
	uCuisine=cuisineInput
	uStars=starsInput
	uDistance=distInput
	uPriority1=priority1Input
	uPriority2=priority2Input
	uPriority3=priority3Input

	[uPriceValue,uStarsValue,uDistanceValue,uCuisineValue] = calculateChoiceValues(uPrice, uCuisine, uStars, uDistance)
	[priceW, cuisineW, starsW, distanceW] = calculateWeights(uPriority1, uPriority2, uPriority3, priceW, cuisineW, starsW, distanceW)
	for i in range(0,size):
		#price 
		if(abs(F[i].price-uPriceValue)==1):
			score[i]+=priceW*3
		elif(abs(F[i].price-uPriceValue)==2):
			score[i]+=priceW*6
		
		#stars
		if(uStarsValue!=-1):
			if(abs(F[i].stars-uStarsValue)==1):
				score[i]+=starsW*3
			elif(abs(F[i].stars-uStarsValue)==2):
				score[i]+=starsW*6
		
		#cuisine
		if(abs(F[i].cuisine-uCuisineValue)==1):
			score[i]+=cuisineW*3
		elif(abs(F[i].cuisine-uCuisineValue)==2):
			score[i]+=cuisineW*5
		elif(abs(F[i].cuisine-uCuisineValue)==3):
			score[i]+=cuisineW*7
		elif(abs(F[i].cuisine-uCuisineValue)==4):
			score[i]+=cuisineW*8
		
		#distance
		#d=math.sqrt((uPosX-F[i].pointX)^2+(uPosY-F[i].pointY)^2)
		d=abs((uPosX-F[i].pointX)+abs(uPosY-F[i].pointY))
		if(uDistanceValue==0):
			if(d>1000 and d<=5000):
				score[i]+=distanceW*3
			elif(d>5000):
				score[i]+=distanceW*6
		elif(uDistanceValue==1):
			if(d>5000):
				score[i]+=distanceW*3

	minPos=0
	minValue=score[0]
	for i in range(0, len(score)):
		print(i)
		if(score[i]<minValue):
			print("im in")
			print(i)
			minPos=i
			minValue=score[i]

	print(F[minPos].Name)
	return [minPos,F,"{0:.2f}".format(minValue)]






