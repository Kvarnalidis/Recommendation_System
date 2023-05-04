from django import forms


Rating_Choice= [
	('0','------'),
    ('n', 'Negative'),
    ('p', 'Positive'),
    ('op', 'Overwhelmingly Positive'),
]
Content_Choice= [
	('0','------'),
    ('b', 'Building'),
    ('m', 'Monument'),
    ('z', 'Zoo'),
    ('np', 'National Park'),
    ('fm', 'Forest/Mountain'),
]
Time_Choice= [
	('0','------'),
    ('s', 'Short (under an hour)'),
    ('a', 'Average (over an hour/under two hours)'),
    ('l','Long (over two hours)'),
]
Distance_Choice=[
	('0','------'),
	('close','Under 1km'),
	('avg','Under 5km'),
	('far','Over 5km'),
]
Priority_Choice=[
	('0','------'),
	('rating','Rating'),
	('content','Content'),
	('time','Time'),
	('dist','Distance'),
]    

class SightChoiceForm(forms.Form):
	rating_choice= forms.CharField(label='What is the desired rating?', widget=forms.Select(choices=Rating_Choice))
	content_choice= forms.CharField(label='What is your content choice?', widget=forms.Select(choices=Content_Choice))
	time_choice= forms.CharField(label='How long would you want your tour to be?', widget=forms.Select(choices=Time_Choice))
	distance_choice= forms.CharField(label='How far away?', widget=forms.Select(choices=Distance_Choice))
	priority_choice1= forms.CharField(label='1st priority ?', widget=forms.Select(choices=Priority_Choice))
	priority_choice2= forms.CharField(label='2nd priority', widget=forms.Select(choices=Priority_Choice))
	priority_choice3= forms.CharField(label='3rd priority?', widget=forms.Select(choices=Priority_Choice))

