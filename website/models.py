from django.db import models


class Log(models.Model):
	obj = models.CharField(max_length=64)
	date = models.DateTimeField()
	message = models.CharField(max_length=512)


class Config(models.Model):
	key = models.CharField(max_length=32)
	value = models.CharField(max_length=256)


class Profile(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='user_profile')
	messages = models.ManyToManyField('chat.Message', related_name='user_messages', blank=True)
	rooms = models.ManyToManyField('chat.Room', related_name='user_rooms', blank=True)
	friends = models.ManyToManyField('self', blank=True)
	banned = models.BooleanField(default=False)
	monitored = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user.get_username()}'


class Ban(models.Model):
	user = models.ForeignKey('website.Profile', on_delete=models.CASCADE, related_name='ban_user')
	reason = models.CharField(max_length=32)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()




