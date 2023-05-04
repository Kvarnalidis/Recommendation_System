from django import forms


Price_Choice= [
	('0','------'),
    ('c', 'Cheap'),
    ('a', 'Average'),
    ('e', 'Expensive'),
]

Theme_Choice= [
	('0','------'),
    ('s', 'Science'),
    ('m', 'Military'),
    ('h', 'History'),
    ('a', 'Art'),
    ('nh', 'Natural history'),
]
Discount_Choice= [
	('0','------'),
    ('y', 'Yes'),
    ('n', 'No'),
]
Distance_Choice=[
	('0','------'),
	('close','Under 1km'),
	('avg','Under 5km'),
	('far','Over 5km'),
]


Priority_Choice=[
	('0','------'),
	('theme','Theme'),
	('price','Price'),
	('discount','Discount Availability'),
	('dist','Distance'),
]    

class MuseumChoiceForm(forms.Form):
	price_choice= forms.CharField(label='What price do you prefer?', widget=forms.Select(choices=Price_Choice))
	theme_choice= forms.CharField(label='What theme do you prefer?', widget=forms.Select(choices=Theme_Choice))
	discount_choice= forms.CharField(label='Do you want discount availability', widget=forms.Select(choices=Discount_Choice))
	distance_choice= forms.CharField(label='How far away?', widget=forms.Select(choices=Distance_Choice))
	priority_choice1= forms.CharField(label='1st priority ?', widget=forms.Select(choices=Priority_Choice))
	priority_choice2= forms.CharField(label='2nd priority', widget=forms.Select(choices=Priority_Choice))
	priority_choice3= forms.CharField(label='3rd priority?', widget=forms.Select(choices=Priority_Choice))

