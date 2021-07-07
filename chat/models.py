from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
	text = models.TextField(null=True, blank=True)
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text


class BannedUser(models.Model):
	ban_creator = models.ForeignKey(User, related_name='ban_creator', on_delete=models.CASCADE)
	ban_target = models.ForeignKey(User, related_name='ban_target', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.ban_target} has banned {self.ban_target}"