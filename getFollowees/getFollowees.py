import sys
import simplejson as json
#--------------------------------
#create your own file: tokens.py
#with follow lines:
#   ACCESS_TOKEN = 'your tokens'
#   ACCESS_SECRET = 'your access secret'
#   CONSUMER_KEY = 'your consumer key'
#   CONSUMER_SECRET = 'your consumer secret'
#-------------------------------
import tokens
import argparse
import tweepy
from time import sleep

def getFolloweesFromId(user_id):
    # Setup tweepy to authenticate with Twitter credentials:
    auth = tweepy.OAuthHandler(tokens.CONSUMER_KEY, tokens.CONSUMER_SECRET)
    auth.set_access_token(tokens.ACCESS_TOKEN, tokens.ACCESS_SECRET)
    # Create the api to connect to twitter with your creadentials
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    dic ={}
    dic['user_id'] = user_id
    try:
        dic['followees'] = requestToFriendsList(api,user_id)
    except Exception as e:
        print(e)
    outFile = open(str(user_id)+'Followees.txt','w')
    json.dump(dic,outFile,indent=4)


#create a file that contains all followees of the users in the retweets file
def getFollowees(fileContent):
    # Setup tweepy to authenticate with Twitter credentials:
    auth = tweepy.OAuthHandler(tokens.CONSUMER_KEY, tokens.CONSUMER_SECRET)
    auth.set_access_token(tokens.ACCESS_TOKEN, tokens.ACCESS_SECRET)

    # Create the api to connect to twitter with your creadentials
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    #load the json from the file
    retweets = json.loads(fileContent)

    retweet_id = retweets[0]['retweeted_status']['id']
    outFile = open('../samples/'+str(retweet_id)+'/followees.txt','w')

    #this variable contains the output file contains
    output=[]
    i = 0
    for retweet in retweets:
        if (i == 4):
            break
        dic = {}
        dic['user_id'] = retweet['user']['id']
        try:
            dic['followees'] = requestToFriendsList(api,retweet['user']['id'])
        except tweepy.TweepError as e:
            if e == "[{u'message': u'Sorry, that page does not exist.', u'code': 34}]":
                continue
            else :
                print(e)
                print("user id invalid , check it :",retweet['user']["id"])
                continue
        print(dic)
        print('============================================================================================================================')
        output.append(dic)

    json.dump(output,outFile,indent=4)
    outFile.close()
    print("a file is generated in sample/"+str(retweet_id)+'/ folder')

def requestToFriendsList(api,user_id):
#---------------------------------------------------------------------------------------------------------------------
# Twitter API development use pagination for Iterating through timelines, user lists, direct messages, etc.
# To help make pagination easier and Tweepy has the Cursor object.
# See the documentation of Tweepy, if you want to understand
#---------------------------------------------------------------------------------------------------------------------
    list_of_followees = []
    current_cursor = tweepy.Cursor(api.friends_ids,user_id=user_id , count=5000)
    current_followees = current_cursor.iterator.next()
    list_of_followees.extend(current_followees)
    next_cursor_id = current_cursor.iterator.next_cursor

    while(next_cursor_id!=0):
            current_cursor = tweepy.Cursor(api.friends_ids,user_id=user_id , count=5000,cursor=next_cursor_id)
            current_followees=current_cursor.iterator.next()
            list_of_followees.extend(current_followees)
            next_cursor_id = current_cursor.iterator.next_cursor
    return list_of_followees




if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', dest='id',help='id of tweet user')
    parser.add_argument('--file',dest='filepath',help='the file path that contains all retweets ')
    args = parser.parse_args()
    if(args.filepath):
         #open the file
         filename = str(args.filepath)
         try :
             fil = open(filename,'r')
         except:
             print('error, can not open the file ')
             exit(0)
         getFollowees(fil.read())

    elif(args.id):
        getFolloweesFromId(int(args.id))

    else:
        print("error, see help")
        exit(0)
