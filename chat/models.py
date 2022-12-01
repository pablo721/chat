from django.db import models
import datetime


class Chat(models.Model):
	owner = models.ForeignKey('website.Account', on_delete=models.CASCADE, related_name='chat_owner', null=False)
	chat_name = models.CharField(max_length=32, null=True, default='Chat')
	creation_date = models.DateTimeField()
	private = models.BooleanField(default=True)
	users = models.ManyToManyField('website.Account', related_name='users_chats', blank=True)

	def __str__(self):
		return self.chat_name + ' (' + str(self.id) + ')'

class Message(models.Model):
	sender = models.ForeignKey('website.Account', on_delete=models.CASCADE, related_name='message_sender')
	chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE, related_name='chat_messages', null=True)
	content = models.TextField(max_length=1000, null=True)
	timestamp = models.DateTimeField(blank=True, null=True)
	sent = models.BooleanField(default=False)
	delivered = models.BooleanField(default=False)
	seen = models.BooleanField(default=False)
	destruct_timer = models.IntegerField(null=True)



	@property
	def remaining(self):
		if self.destruct_timer:
			return ((self.timestamp.timestamp() + self.destruct_timer) - datetime.datetime.now().timestamp()).__round__(0)


	def __str__(self):
		return str(self.timestamp) + ' ' + self.sender.user.get_username() + ': ' + str(self.content)











