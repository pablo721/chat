from django.db import models


class Log(models.Model):
	obj = models.CharField(max_length=64)
	date = models.DateTimeField()
	message = models.CharField(max_length=512)


class Config(models.Model):
	key = models.CharField(max_length=32)
	value = models.CharField(max_length=256)


class Account(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='user_account')
	friends = models.ManyToManyField('self', blank=True)
	signup_location = models.CharField(max_length=32, blank=True, null=True)
	signup_ip = models.CharField(max_length=64, blank=True, null=True)
	# banned = models.BooleanField(default=False, blank=True)
	# monitored = models.BooleanField(default=False, blank=True)


	def __str__(self):
		return f'{self.user.get_username()}'


class Ban(models.Model):
	user = models.ForeignKey('website.Account', on_delete=models.CASCADE, related_name='ban_user')
	reason = models.CharField(max_length=32)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()




