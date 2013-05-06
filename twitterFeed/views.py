from settings import *
import tweepy
from django.http import HttpResponseRedirect, HttpResponse
from models import *
import pickle
from base64 import b64encode, b64decode
from django.utils import feedgenerator
import datetime
from django.utils import timezone

def home(request, token = None):
	auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, request.build_absolute_uri())

	if token != None and TwitterAuthToken.objects.filter(key__exact = token).count() > 0:
		tat = TwitterAuthToken.objects.get(key = token)
		auth.set_access_token(tat.key, tat.secret)
	else:
		verifier = request.GET.get('oauth_verifier', None)
		if verifier == None:
			redirect_url = auth.get_authorization_url()
			request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
			return HttpResponseRedirect(redirect_url)
		else:
			token = request.session.get('request_token')
			request.session.delete('request_token')
			auth.set_request_token(token[0], token[1])
			auth.get_access_token(verifier)

			tat = TwitterAuthToken.objects.filter(key__exact = auth.access_token.key)
			if tat.count() == 0:
				tat = TwitterAuthToken(key = auth.access_token.key)
			else:
				tat = tat[0]
			tat.secret = auth.access_token.secret
			tat.save()
			request.session['tat'] = tat.id
			return HttpResponseRedirect("/%s"%tat.key)

	now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
	
	checktime = now - datetime.timedelta(minutes = 10)
	if tat.last == None or tat.timeline == None or len(tat.timeline) == 0 or tat.last < checktime:
		api = tweepy.API(auth)
		tat.timeline = b64encode(pickle.dumps(api.home_timeline(count = 200)))
		tat.username = auth.get_username()
		tat.last = now
		tat.save()

	feed = feedgenerator.Rss201rev2Feed(
		title="Abbreviated Twitter links feed for %s"%tat.username,
		link=request.build_absolute_uri(),
		description = ""
	)
	for status in pickle.loads(b64decode(tat.timeline)):
		if status.in_reply_to_status_id != None:
			continue
		if len(status.entities["urls"]) == 0:
			continue
		while hasattr(status, "retweeted_status") and status.retweeted_status != None:
			status = status.retweeted_status
		
		urls = status.entities["urls"]

		badsites = ["4sq.com", "instagram.com"]

		while len(urls) > 0:
			bad = [urls[0]["expanded_url"].find(b) != -1 for b in badsites]
			bad = reduce(lambda x,y: x or y, bad, False)
			if bad:
				urls = urls[1:]
			else:
				break

		if len(urls) > 0:
			for u in urls:
				status.text = status.text[:u["indices"][0]] + u["expanded_url"] + status.text[u["indices"][1]:]
			feed.add_item(title = status.text, link = urls[0]["expanded_url"], description = "")

	return HttpResponse(feed.writeString("utf-8"))
