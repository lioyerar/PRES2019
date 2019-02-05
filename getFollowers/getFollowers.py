import sys
import simplejson as json
#--------------------------------
#create your own file: tokens.py
#with follow lines:
#   ACCESS_TOKEN = 'your tokens'
#   ACCESS_SECRET = 'your access secret'
#   CONSUMER_KEY = 'your consumer key'
#   CONSUMER_SECRET = 'your consumer secret'
#--------------------------------
import tokens

import tweepy
from time import sleep


#create a file that contains all followers of the users in the retweets file
def getFollowers(fileContent):
    # Setup tweepy to authenticate with Twitter credentials:
    auth = tweepy.OAuthHandler(tokens.CONSUMER_KEY, tokens.CONSUMER_SECRET)
    auth.set_access_token(tokens.ACCESS_TOKEN, tokens.ACCESS_SECRET)

    # Create the api to connect to twitter with your creadentials
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    #load the json from the file
    retweets = json.loads(fileContent)

    retweet_id = retweets[0]['retweeted_status']['id']
    outFile = open('../samples/'+str(retweet_id)+'/followers.txt','w')

    #this variable contains the output file contains
    output=[]
    for retweet in retweets:
        list_of_followers = []
        dic = {}
        dic['user_id'] = retweet['user']['id']

   #---------------------------------------------------------------------------------------------------------------------
   # Twitter API development use pagination for Iterating through timelines, user lists, direct messages, etc.
   # To help make pagination easier and Tweepy has the Cursor object.
   # See the documentation of Tweepy, if you want to understand
   #---------------------------------------------------------------------------------------------------------------------
        try:
              current_cursor = tweepy.Cursor(api.followers_ids,user_id=int(retweet['user']['id']), count=5000)
              current_followers = current_cursor.iterator.next()
              list_of_followers.extend(current_followers)
              next_cursor_id = current_cursor.iterator.next_cursor

        except tweepy.TweepError,e:
            if e == "[{u'message': u'Sorry, that page does not exist.', u'code': 34}]":
                print("user id invalid , check it :",retweet['user']["id"])
                continue
            else :
                print e
                continue

        while(next_cursor_id!=0):
            current_cursor = tweepy.Cursor(api.followers_ids, user_id=retweet['id'], count=5000,cursor=next_cursor_id)
            current_followers=current_cursor.iterator.next()
            list_of_followers.extend(current_followers)
            next_cursor_id = current_cursor.iterator.next_cursor
        print(list_of_followers)
        dic['followers'] = list_of_followers
        output.append(dic)
        print('sleep 1 min ')
        sleep(60)

    json.dump(output,outFile,indent=4)
    outFile.close()
    print("a file is generated in sample/"+str(retweeted_id)+'/ folder')



if __name__=='__main__':
#check the retweets file
    if (not sys.argv[1]):
        print('you need input a retweets file (ie <id_of_retweets.txt> in your samples folder )')
        exit(0)
#open the file
    filename = str(sys.argv[1])
    try :
        fil = open(filename,'r')

    except:
        print('error, can not open the file ')
    getFollowers(fil.read())
