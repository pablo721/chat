from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import Keyword, Watchlist, FlaggedMessage
from website.models import Profile, Ban
import datetime


class SpybotView(TemplateView):
	template_name = 'spybot/spybot.html'


	def post(self, request, *args, **kwargs):
		if 'ban' in str(request.POST) and 'user_id' in str(request.POST):
			profile = request.user.user_profile
			now = datetime.datetime.now()
			end_date = now + datetime.timedelta(days=request.POST['days'])
			Ban.objects.create(user=profile, reason=request.POST['reason'], start_date=now, end_date=end_date)
			profile.banned = True
			profile.save()
			return HttpResponseRedirect('spybot:spybot')

		elif 'monitor' in str(request.POST):


			if 'user_id' in str(request.POST):
				pass
			elif 'room_id' in str(request.POST):
				pass
			elif 'friend_id' in str(request.POST):
				pass


	def get_context_data(self, **kwargs):
		pass



class MonitorView(SpybotView):
	template_name = 'spybot/_monitor.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)



