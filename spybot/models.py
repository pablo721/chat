from django.db import models


class Keyword(models.Model):
	keyword = models.CharField(max_length=64)
	forbidden = models.BooleanField(default=False)

	def __str__(self):
		return self.keyword


class Watchlist(models.Model):
	name = models.CharField(max_length=32, blank=False)
	creator = models.ForeignKey('website.Profile', related_name='watchlist_creator', on_delete=models.CASCADE)
	users = models.ManyToManyField('website.Profile', related_name='watchlist_profiles')
	rooms = models.ManyToManyField('chat.Room', related_name='watchlist_rooms')
	keywords = models.ManyToManyField('spybot.Keyword', related_name='watchlist_keywords')
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class FlaggedMessage(models.Model):
	sender = models.ForeignKey('website.Profile', on_delete=models.CASCADE, related_name='flagged_message_user')
	message = models.ForeignKey('chat.Message', on_delete=models.CASCADE, related_name='flagged_message_message')
	flag_date = models.DateTimeField()
	reason = models.CharField(max_length=64)


