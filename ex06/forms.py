from django import forms
from django.forms.widgets import Textarea

class MovieForm(forms.Form):
	def __init__(self, *args, choices=[], **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['movie_name'].widget = forms.Select(choices=choices)

	movie_name = forms.CharField(
		required=True,
		max_length=64,
		widget=forms.Select(),
	)

	opening_crawl = forms.CharField(
		widget=forms.Textarea()
	)
