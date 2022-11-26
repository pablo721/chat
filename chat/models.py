from django.db import models
import datetime


class Message(models.Model):
	sender = models.ForeignKey('website.Profile', on_delete=models.CASCADE, unique=False, related_name='message_sender',
							    blank=True)
	recipient_id = models.IntegerField(default=-1)
	room_id = models.IntegerField(default=-1)
	content = models.TextField(max_length=1000, blank=False)
	timestamp = models.DateTimeField(blank=True)
	sent = models.BooleanField(default=False)
	delivered = models.BooleanField(default=False)
	seen = models.BooleanField(default=False)
	encrypted = models.BooleanField(default=False)
	encryption_algorithm = models.CharField(max_length=3, choices=enumerate(['AES', 'RSA']))
	destruct_timer = models.IntegerField(blank=True, null=True, default=50)
	watchlists = models.ManyToManyField('spybot.Watchlist', related_name='message_watchlists')
	flagged = models.BooleanField(default=False)

	def __str__(self):
		return str(self.timestamp) + ' ' + self.sender.user.get_username() + ': ' + str(self.content)


class Room(models.Model):
	creator = models.ForeignKey('website.Profile', on_delete=models.CASCADE, related_name='room_creator')
	room_name = models.CharField(max_length=32)
	creation_date = models.DateTimeField()
	private = models.BooleanField(default=False)
	users = models.ManyToManyField('website.Profile', related_name='room_users', blank=True)
	censored = models.BooleanField(default=False)


	def __str__(self):
		return self.room_name








