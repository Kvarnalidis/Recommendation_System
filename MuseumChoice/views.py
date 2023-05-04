from django.shortcuts import render,redirect
from .forms import MuseumChoiceForm


#imports for algorithm 
from Museums.models import Museums
import math

# Create your views here.
def museum_choice_view(request):
	next =request.GET.get('next')
	form =MuseumChoiceForm(request.POST)
	if form.is_valid():
		price =form.cleaned_data['price_choice']
		dist = form.cleaned_data['distance_choice']
		theme =form.cleaned_data['theme_choice']
		discount= form.cleaned_data['discount_choice']
		priority1=form.cleaned_data['priority_choice1']
		priority2=form.cleaned_data['priority_choice2']
		priority3=form.cleaned_data['priority_choice3']
		[position,M,score] = algorithm(price,dist,theme,discount,priority1,priority2,priority3)
		print(position)
		[priceDB,themeDB,discountDB] = getDBvalues(position,M)
		context1={
			'name':"Museum Name: "+M[position].Name,
			'image':M[position].Image,
			'description':"Description: "+M[position].description,
			'location':"Address: "+M[position].Location,
			'score':"Penalty score: "+str(score),
			'input1':"Price range: "+priceDB,
			'input2':"Museum theme: "+themeDB,
			'input3':"Discount availability: "+discountDB
		}
		if next:
			return redirect(next)
		return render(request,"resaults.html",context1)

	context={
		'form':form
	}

	return render(request,"museums.html",context)



#get the appropriate info from db in strings
def getDBvalues(position,M):
	if(M[position].price==0):
		priceDB="Cheap"
	elif(M[position].price==1):
		priceDB="Average"
	else:
		priceDB="Expensive"

	if(M[position].theme==0):
		themeDB="Military"
	elif(M[position].theme==1):
		themeDB="History"
	elif(M[position].theme==2):
		themeDB="Natural History"
	elif(M[position].theme==3):
		themeDB="Science"
	else:
		themeDB="Art"

	if(M[position].discountAvailability==0):
		discountDB="Available"
	else:
		discountDB="Not Available"
	return [priceDB,themeDB,discountDB]


#calculate the corresponding values for comparison with the database
def calculateChoiceValues(uPrice, uTheme, uDiscount, uDistance):
	#price
	if(uPrice=="c"):
		uPriceValue=0
	elif(uPrice=="a"):
		uPriceValue=1
	elif(uPrice=="0"):
		uPriceValue=-10
	else:
		uPriceValue=2
	
	#discount
	if(uDiscount=="y"):
		uDiscountValue=0
	elif(uDiscount=="n"):
		uDiscountValue=1
	else:
		uDiscountValue=-10
	
	#distance
	if(uDistance=="close"):
		uDistanceValue=0
	elif(uDistance=="avg"):
		uDistanceValue=1
	elif(uDistance=="0"):
		uDistanceValue=-10
	else:
		uDistanceValue=2
	
	#theme
	if(uTheme=="m"):
		uThemeValue=0
	elif(uTheme=="h"):
		uThemeValue=1
	elif(uTheme=="nh"):
		uThemeValue=2
	elif(uTheme=="s"):
		uThemeValue=3
	elif(uTheme=="0"):
		uThemeValue=-10
	else:
		uThemeValue=4
	return [uPriceValue,uDiscountValue,uDistanceValue,uThemeValue]


#calculate weights according to the priorities
def calculateWeights(uPriority1, uPriority2, uPriority3, priceW, themeW, discountW, distanceW):
	if(uPriority1=="price"):
		priceW=priceW+1
	elif(uPriority1=="theme"):
		themeW=themeW+1
	elif(uPriority1=="discount"):
		discountW=discountW+1
	elif(uPriority1=="dist"):
		distanceW=distanceW+1

	if(uPriority2=="price"):
		priceW=priceW+0.6
	elif(uPriority2=="theme"):
		themeW=themeW+0.6
	elif(uPriority2=="discount"):
		discountW=discountW+0.6
	elif(uPriority2=="dist"):
		distanceW=distanceW+0.6
		
	if(uPriority3=="price"):
		priceW=priceW+0.2
	elif(uPriority3=="theme"):
		themeW=themeW+0.2
	elif(uPriority3=="discount"):
		discountW=discountW+0.2
	elif(uPriority3=="dist"):
		distanceW=distanceW+0.2
	return [priceW, themeW, discountW, distanceW]



def algorithm(priceInput, distInput, themeInput, discountInput, priority1Input, priority2Input, priority3Input):
	priceW=1.0
	themeW=1.0
	distanceW=1.0
	discountW=1.0
	score=[0.0]

	M=Museums.objects.all()
	size=M.count()

	for i in range(1,size):
		score.append(0)

	uPosX=0
	uPosY=0
	uPrice=priceInput
	uTheme=themeInput
	uDiscount=discountInput
	uDistance=distInput
	uPriority1=priority1Input
	uPriority2=priority2Input
	uPriority3=priority3Input

	[uPriceValue,uDiscountValue,uDistanceValue,uThemeValue] = calculateChoiceValues(uPrice, uTheme, uDiscount, uDistance)
	[priceW, themeW, discountW, distanceW] = calculateWeights(uPriority1, uPriority2, uPriority3, priceW, themeW, discountW, distanceW)
	for i in range(0,size):
		#price 
		if(abs(M[i].price-uPriceValue)==1):
			score[i]+=priceW*3
		elif(abs(M[i].price-uPriceValue)==2):
			score[i]+=priceW*6
		
		#discount
		if(abs(M[i].discountAvailability-uDiscountValue)==1):
			score[i]+=discountW*5
		
		#theme
		if(abs(M[i].theme-uThemeValue)==1):
			score[i]+=themeW*3
		elif(abs(M[i].theme-uThemeValue)==2):
			score[i]+=themeW*5
		elif(abs(M[i].theme-uThemeValue)==3):
			score[i]+=themeW*7
		elif(abs(M[i].theme-uThemeValue)==4):
			score[i]+=themeW*8
		
		#distance
		#d=math.sqrt((uPosX-M[i].pointX)^2+(uPosY-M[i].pointY)^2)
		d=abs((uPosX-M[i].pointX)+abs(uPosY-M[i].pointY))
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

	print(M[minPos].Name)
	return [minPos,M,"{0:.2f}".format(minValue)]