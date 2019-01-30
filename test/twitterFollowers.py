#! /usr/bin/python
#coding:utf-8
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

# Variables that contains the user credentials to access Twitter API
# put your tokens
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = 'jI8DrTIWfrwyVmnQvJk73zXWcw0iMlX7YsfW8vaSo3b9aeZ6zM'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= Ture;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
# The following loop will print most recent statuses, including retweets, posted by the authenticating user and that user’s friends.
# This is the equivalent of /timeline/home on the Web.
#---------------------------------------------------------------------------------------------------------------------

#for status in tweepy.Cursor(api.home_timeline).items(200):
#	print(status._json)



#---------------------------------------------------------------------------------------------------------------------
# Twitter API development use pagination for Iterating through timelines, user lists, direct messages, etc.
# To help make pagination easier and Tweepy has the Cursor object.
#---------------------------------------------------------------------------------------------------------------------


#list of followers
# Get the full list of followers of a particular user
list_of_followers=[]

current_cursor = tweepy.Cursor(api.followers_ids, screen_name="HugoMagnaudet", count=5000)
current_followers = current_cursor.iterator.next()
list_of_followers.extend(current_followers)
next_cursor_id = current_cursor.iterator.next_cursor

while(next_cursor_id!=0):
	current_cursor = tweepy.Cursor(self.api.followers_ids, screen_name="cocoweixu", count=5000,cursor=next_cursor_id)
	current_followers=current_cursor.iterator.next()
	list_of_followers.extend(current_followers)
	next_cursor_id = current_cursor.iterator.next_cursor

# Get a particular user's timeline (up to 200 of his/her most recent tweets)
status_cursor = tweepy.Cursor(api.user_timeline, screen_name="billybob", count=200,tweet_mode='extended')
status_list = status_cursor.iterator.next()

#user=api.get_user(list_of_followers[0])
#print(user.timeline())
#print(api.rate_limit_status())
print(list_of_followers)
