from django.db import models

class TwitterAuthToken(models.Model):
	key = models.CharField(max_length=200)
	secret = models.CharField(max_length=200)
	username = models.CharField(max_length=50)
	timeline = models.TextField()
	last = models.DateTimeField(null = True, blank = True)

	def __str__(self):
		return "key: '%s' secret: '%s'"%(self.key, self.secret)
