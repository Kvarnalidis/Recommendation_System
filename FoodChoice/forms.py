from django import forms


Price_Choice= [
	('0','-----'),
    ('c', 'Cheap'),
    ('a', 'Average'),
    ('e', 'Expensive'),
]

Star_Choice= [
	('0','-----'),
    ('one', '1'),
    ('two', '2'),
    ('three', '3'),
]
Cuisine_Choice= [
	('0','-----'),
    ('g', 'Greek'),
    ('c', 'Chinese'),
    ('l', 'Lebanese'),
    ('i','Italian'),
    ('f','Fast Food'),
]
Distance_Choice=[
	('0','-----'),
	('close','Under 1km'),
	('avg','Under 5km'),
	('far','Over 5km'),
]


Priority_Choice=[
	('0','-----'),
	('cuisine','Cuisine'),
	('price','Price'),
	('stars','Michelin Stars'),
	('dist','Distance'),
]    

class FoodChoiceForm(forms.Form):
	price_choice= forms.CharField(label='What price do you prefer?', widget=forms.Select(choices=Price_Choice))
	star_choice= forms.CharField(label='How many Michelin stars?', widget=forms.Select(choices=Star_Choice))
	cuisine_choice= forms.CharField(label='What type of cuisine?', widget=forms.Select(choices=Cuisine_Choice))
	distance_choice= forms.CharField(label='How far away?', widget=forms.Select(choices=Distance_Choice))
	priority_choice1= forms.CharField(label='1st priority', widget=forms.Select(choices=Priority_Choice))
	priority_choice2= forms.CharField(label='2nd priority', widget=forms.Select(choices=Priority_Choice))
	priority_choice3= forms.CharField(label='3rd priority', widget=forms.Select(choices=Priority_Choice))