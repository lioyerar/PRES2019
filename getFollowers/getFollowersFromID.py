#! /usr/bin/python
#coding:utf-8
# Import the necessary package to process data in JSON format
import json
# Import the tweepy library
import tweepy
import sys
import tokens
# Variables that contains the user credentials to access Twitter API

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(tokens.CONSUMER_KEY, tokens.CONSUMER_SECRET)
auth.set_access_token(tokens.ACCESS_TOKEN, tokens.ACCESS_SECRET)

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
dic = {}
list_of_followers = []
dic['user_id'] = int(sys.argv[1])

current_cursor = tweepy.Cursor(api.followers_ids,user_id=int(sys.argv[1]),count=5000)
current_followers = current_cursor.iterator.next()
list_of_followers.extend(current_followers)
next_cursor_id = current_cursor.iterator.next_cursor

while(next_cursor_id!=0):
	current_cursor = tweepy.Cursor(self.api.followers_ids,user_id=sys.argv[1] , count=5000,cursor=next_cursor_id)
	current_followers=current_cursor.iterator.next()
	list_of_followers.extend(current_followers)
	next_cursor_id = current_cursor.iterator.next_cursor

dic['followers'] = list_of_followers
outFile = open(sys.argv[1]+'Followers.txt','w')
json.dump(dic,outFile,indent=4)
