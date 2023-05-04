from django.shortcuts import render,redirect
from .forms import SightChoiceForm
#imports for algorithm 
from Shights.models import Sights
import math
# Create your views here.
def sight_choice_view(request):
	next =request.GET.get('next')
	form =SightChoiceForm(request.POST)
	if form.is_valid():
		rating =form.cleaned_data['rating_choice']
		dist = form.cleaned_data['distance_choice']
		time =form.cleaned_data['time_choice']
		content= form.cleaned_data['content_choice']
		priority1=form.cleaned_data['priority_choice1']
		priority2=form.cleaned_data['priority_choice2']
		priority3=form.cleaned_data['priority_choice3']
		[position,S,score] = algorithm(rating,dist,content,time,priority1,priority2,priority3)
		[ratingDB,contentDB,timeDB] = getDBvalues(position,S)
		print(position)
		context1={
			'name':"Sight Name: "+S[position].Name,
			'image':S[position].Image,
			'description':"Description: "+S[position].description,
			'location':"Address: "+S[position].Location,
			'score':"Penalty score: "+str(score),
			'input1':"Overall rating: "+ratingDB,
			'input2':"Sight content: "+contentDB,
			'input3':"Sight approximate time required: "+timeDB
		}
		if next:
			return redirect(next)
		return render(request,"resaults.html",context1)

	context={
		'form':form
	}

	return render(request,"sights.html",context)




#get the appropriate info from db in strings
def getDBvalues(position,S):
	if(S[position].rating==0):
		ratingDB="Negative"
	elif(S[position].rating==1):
		ratingDB="Positive"
	else:
		ratingDB="Overwhelmingly Positive"

	if(S[position].content==0):
		contentDB="Monument"
	elif(S[position].content==1):
		contentDB="Building"
	elif(S[position].content==2):
		contentDB="Natural Park"
	elif(S[position].content==3):
		contentDB="Zoo"
	else:
		contentDB="Forest/Mountain"

	if(S[position].time==0):
		timeDB="Short (under an hour)"
	elif(S[position].time==1):
		timeDB="Average (over an hour/under two hours)"
	else:
		timeDB="Long (over two hours)"
	return [ratingDB,contentDB,timeDB]


#calculate the corresponding values for comparison with the database
def calculateChoiceValues(uRating, uContent, uTime, uDistance):
	#rating
	if(uRating=="n"):
		uRatingValue=0
	elif(uRating=="p"):
		uRatingValue=1
	elif(uRating=="0"):
		uRatingValue=-10
	else:
		uRatingValue=2
	
	#time
	if(uTime=="s"):
		uTimeValue=0
	elif(uTime=="a"):
		uTimeValue=1
	elif(uTime=="l"):
		uTimeValue=2
	else:
		uTimeValue=-10
	
	#distance
	if(uDistance=="close"):
		uDistanceValue=0
	elif(uDistance=="avg"):
		uDistanceValue=1
	elif(uDistance=="0"):
		uDistanceValue=-10
	else:
		uDistanceValue=2
	
	#content
	if(uContent=="m"):
		uContentValue=0
	elif(uContent=="b"):
		uContentValue=1
	elif(uContent=="np"):
		uContentValue=2
	elif(uContent=="z"):
		uContentValue=3
	elif(uContent=="0"):
		uContentValue=-10
	else:
		uContentValue=4
	return [uRatingValue,uTimeValue,uDistanceValue,uContentValue]


#calculate weights according to the priorities
def calculateWeights(uPriority1, uPriority2, uPriority3, ratingW, contentW, timeW, distanceW):
	if(uPriority1=="rating"):
		ratingW=ratingW+1
	elif(uPriority1=="content"):
		contentW=contentW+1
	elif(uPriority1=="time"):
		timeW=timeW+1
	elif(uPriority1=="dist"):
		distanceW=distanceW+1

	if(uPriority2=="rating"):
		ratingW=ratingW+0.6
	elif(uPriority2=="content"):
		contentW=contentW+0.6
	elif(uPriority2=="time"):
		timeW=timeW+0.6
	elif(uPriority2=="dist"):
		distanceW=distanceW+0.6
		
	if(uPriority3=="rating"):
		ratingW=ratingW+0.2
	elif(uPriority3=="content"):
		contentW=contentW+0.2
	elif(uPriority3=="time"):
		timeW=timeW+0.2
	elif(uPriority3=="dist"):
		distanceW=distanceW+0.2
	return [ratingW, contentW, timeW, distanceW]



def algorithm(ratingInput, distInput, contentInput, timeInput, priority1Input, priority2Input, priority3Input):
	ratingW=1.0
	contentW=1.0
	distanceW=1.0
	timeW=1.0
	score=[0.0]

	S=Sights.objects.all()
	size=S.count()

	for i in range(1,size):
		score.append(0)

	uPosX=0
	uPosY=0
	uRating=ratingInput
	uContent=contentInput
	uTime=timeInput
	uDistance=distInput
	uPriority1=priority1Input
	uPriority2=priority2Input
	uPriority3=priority3Input

	[uRatingValue,uTimeValue,uDistanceValue,uContentValue] = calculateChoiceValues(uRating, uContent, uTime, uDistance)
	[ratingW, contentW, timeW, distanceW] = calculateWeights(uPriority1, uPriority2, uPriority3, ratingW, contentW, timeW, distanceW)
	for i in range(0,size):
		#rating 
		if(abs(S[i].rating-uRatingValue)==1):
			score[i]+=ratingW*3
		elif(abs(S[i].rating-uRatingValue)==2):
			score[i]+=ratingW*6
		
		#time
		if(abs(S[i].time-uTimeValue)==1):
			score[i]+=timeW*3
		elif(abs(S[i].time-uTimeValue)==2):
			score[i]+=timeW*6
		#content
		if(abs(S[i].content-uContentValue)==1):
			score[i]+=contentW*3
		elif(abs(S[i].content-uContentValue)==2):
			score[i]+=contentW*5
		elif(abs(S[i].content-uContentValue)==3):
			score[i]+=contentW*7
		elif(abs(S[i].content-uContentValue)==4):
			score[i]+=contentW*8
		
		#distance
		#d=math.sqrt((uPosX-S[i].pointX)^2+(uPosY-S[i].pointY)^2)
		d=abs((uPosX-S[i].pointX)+abs(uPosY-S[i].pointY))
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

	print(S[minPos].Name)
	return [minPos,S,"{0:.2f}".format(minValue)]