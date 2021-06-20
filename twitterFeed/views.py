import tweepy
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
import pickle
from base64 import b64encode, b64decode
from django.utils import feedgenerator
import datetime
from django.utils import timezone
from django_genshi import render_to_response
import os
from functools import reduce

def authenticate(request, token = None):
	auth = tweepy.OAuthHandler(os.environ["TWITTER_CONSUMER_KEY"], os.environ["TWITTER_CONSUMER_SECRET"], request.build_absolute_uri())

	if token != None and TwitterAuthToken.objects.filter(key__exact = token).count() > 0:
		tat = TwitterAuthToken.objects.get(key = token)
		auth.set_access_token(tat.key, tat.secret)
		return auth
	else:
		verifier = request.GET.get('oauth_verifier', None)
		if verifier == None:
			redirect_url = auth.get_authorization_url()
			request.session['request_token'] = auth.request_token
			return HttpResponseRedirect(redirect_url)
		else:
			token = request.session.get('request_token')
			request.session.delete('request_token')
			auth.request_token = token
			auth.get_access_token(verifier)

			tat = TwitterAuthToken.objects.filter(key__exact = auth.access_token)
			if tat.count() == 0:
				tat = TwitterAuthToken(key = auth.access_token)
			else:
				tat = tat[0]
			tat.secret = auth.access_token_secret
			tat.save()
			request.session['tat'] = tat.id
			return HttpResponseRedirect("/%s"%tat.key)

def index(request, token = None):
	ret = authenticate(request, token)
	if isinstance(ret, tweepy.OAuthHandler):
		auth = ret
	else:
		return ret

	api = tweepy.API(auth)
	lists = api.lists_all()

	return render_to_response("index.html", {"lists": lists, "token": token})

def generate_feed(feed, statuses):
	for status in statuses:
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
			feed.add_item(title = "@%s %s" %(status.author.screen_name, status.text), link = urls[0]["expanded_url"], description = "")

def home(request, token = None):
	ret = authenticate(request, token)
	if isinstance(ret, tweepy.OAuthHandler):
		auth = ret
		tat = TwitterAuthToken.objects.get(key = token)
	else:
		return ret
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
	generate_feed(feed, pickle.loads(b64decode(tat.timeline)))
	return HttpResponse(feed.writeString("utf-8"))

def list(request, token, listname):
	ret = authenticate(request, token)
	if isinstance(ret, tweepy.OAuthHandler):
		auth = ret
		tat = TwitterAuthToken.objects.get(key = token)
	else:
		return ret

	listdata = ListData.objects.filter(token = tat, name = listname)
	if len(listdata) == 0:
		listdata = ListData(token = tat, name = listname)
	else:
		listdata = listdata[0]

	now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())

	checktime = now - datetime.timedelta(minutes = 10)
	if listdata.last == None or listdata.content == None or len(listdata.content) == 0 or listdata.last < checktime:
		api = tweepy.API(auth)
		if tat.username == '' or tat.username == None:
			tat.username = auth.get_username()
			tat.save()
		user_id = api.get_user(screen_name = tat.username).id
		listdata.content = b64encode(pickle.dumps(api.list_timeline(slug = listdata.name, count = 200, owner_id = user_id)))
		listdata.last = now
		listdata.save()
	feed = feedgenerator.Rss201rev2Feed(
		title="Abbreviated Twitter links feed for %s - %s "%(tat.username, listdata.name),
		link=request.build_absolute_uri(),
		description = ""
	)
	generate_feed(feed, pickle.loads(b64decode(listdata.content)))
	return HttpResponse(feed.writeString("utf-8"))
