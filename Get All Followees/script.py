#usage :
#   python script.py <fichier contenant la trace>

import json
import sys
import tokens
import tweepy
from time import sleep

def extract(fichier):
    f = open(fichier)
    f = f.readlines()
    users = []
    bool = False
    cpt = 1
    for i in f :
        if bool:
            if "," in i:
                i = i.replace("\"id\":","")
                i = i.replace(",\n","")
                i = i.replace(" ","")
                i = i.replace("}","")
                if i != '':
                    i = int(i)
                if i not in users:
                    users.append(i)
                    print("user",cpt,":",i)
                    cpt+=1
            bool = False
        i = str(i)
        if "user" in i:
            bool = True
    dic = {}
    dic['users'] = users
    f3 = open("output.json","w+")
    json.dump(dic,f3,indent=4)
    f3.close()
    return dic

def getAllFollowers(tab):
    length = len(tab)
    auth = tweepy.OAuthHandler(tokens.CONSUMER_KEY, tokens.CONSUMER_SECRET)
    auth.set_access_token(tokens.ACCESS_TOKEN, tokens.ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    ans = []
    for i in range(3):#len(tab)):
        print("Requesting Followees of",tab[i],",",length-i,"to go...")
        eachFollowers = {}
        list_of_followers = []
        try:
            current_cursor = tweepy.Cursor(api.friends_ids,user_id=tab[i], count=5000)
            current_followers = current_cursor.iterator.next()
            list_of_followers.extend(current_followers)
            next_cursor_id = current_cursor.iterator.next_cursor
            print('sleeping 1 min')
            sleep(60)
        except tweepy.TweepError as e:
            if e == "[{u'message': u'Sorry, that page does not exist.', u'code': 34}]":
                print("user id invalid , check it :",tab[i])
                continue
            else :
                print(e)
                continue
        while(next_cursor_id!=0):
            current_cursor = tweepy.Cursor(api.friends_ids, user_id=tab[i], count=5000,cursor=next_cursor_id)
            current_followers=current_cursor.iterator.next()
            list_of_followers.extend(current_followers)
            next_cursor_id = current_cursor.iterator.next_cursor
            print('sleeping 1 min')
            sleep(60)
        eachFollowers[tab[i]] = list_of_followers
        f3 = open(str(tab[i])+"Followees.json","w+")
        json.dump(eachFollowers,f3,indent=4)
        f3.close()
        ans.append(eachFollowers)
    return ans

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Missing Arguments")
    elif(len(sys.argv) == 2):
        users = extract(sys.argv[1])
        users = users['users']
        print("Got",len(users)," users !\nRequesting API ...")
        eachFollowers = getAllFollowers(users)
        print("Outputing in a json file ...")
        f3 = open("Followees.json","w+")
        json.dump(eachFollowers,f3,indent=4)
        f3.close()
    else:
        print("Too many arguments")
