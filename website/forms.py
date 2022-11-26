from django import forms
from chat.models import Message, Profile, Room


class ScanForm(forms.Form):
	keyword = forms.CharField(max_length=64, blank=False)
	start_date = forms.DateTimeField(blank=True)
	end_date = forms.DateTimeField(blank=True)


class ScanUserForm(ScanForm):
	username = forms.CharField(max_length=32, widget=forms.ChoiceField(choices=()))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].choices = enum([p for p in Profile.objects.all()])


class ScanRoomForm(forms.Form):
	room_name = forms.CharField(max_length=32, widget=forms.ChoiceField(choices=()))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['room_name'].choices = enum([r for r in Room.objects.all()])



