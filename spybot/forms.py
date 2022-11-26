from django import forms
from website.models import Profile
from chat.models import Chat, Room
from .models import Keyword, Watchlist


class MonitorForm(forms.Form):
	target_name = forms.CharField(max_length=32, widget=forms.ChoiceField(choices=[]))
	target_type = forms.CharField(max_length=5, widget=forms.ChoiceField(choices=['User', 'Chat', 'Room']))
	keyword = forms.CharField(max_length=64, widget=forms.ChoiceField(choices=[]))
	watchlist = forms.CharField(max_length=64, widget=forms.ChoiceField(choices=[]))
	all_msgs = forms.BooleanField(required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['keyword'].choices = [keyword.keyword for keyword in Keyword.objects.all()]

		#self.fields['watchlist'].choices = [keyword.keyword for keyword in Keyword.objects.all()]



class BanUserForm(forms.Form):
	username = forms.CharField(max_length=32, widget=forms.ChoiceField(choices=[]))
	reason = forms.CharField(max_length=64, blank=False)
	timeframe = forms.CharField(max_length=5,
								widget=forms.ChoiceField(choices=enumerate(['hour', 'day', 'week', 'month', 'year'])))
	length = forms.IntegerField()


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].choices = [profile for profile in Profile.objects.all()]



class UnbanUserForm(forms.Form):
	username = forms.CharField(max_length=32, widget=forms.ChoiceField(choices=[]))
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].choices = [profile for profile in Profile.objects.all()]