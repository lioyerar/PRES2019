# -*- coding: utf-8 -*-
"""
Created on Saturday Feb 16
@author:SANG
"""


import json
from getFollowers import getFollowees,tokens
import argparse
from threading import *
from graphviz import Digraph
RATE = 3

class Heuristique3:

    #initialise with the given json file name that should contains retweets file.
    def __init__(self,json_file_name):
        self.file_name = json_file_name
        self.retweets = self.load(json_file_name)
        self.origin_author_id = self.retweets[0]['retweeted_status']['user']['id']
        self.rate_users = self.filter_user_rate(self.count_users())

    #load the json file
    def load(self,file_name):
        try:
            json_file = open(file_name,'r')
        except Exception as e:
            print('the file name {} does not exist, check your file'.format(file_name))
            print('terminate the programme ')
            exit(0)
        return json.load(json_file)

    #count the number of users appear in retweets
    #return a dict: key = user's id, and the value = the numbre of this user appear in this file
    def count_users(self):
        dic = {}
        for retweet in self.retweets:
            if(str(retweet['user']['id']) in dic):
                dic[str(retweet['user']['id'])] +=1
            else:
                dic[str(retweet['user']['id'])] = 1
        return dic

    #return a list of users's id that appear more that RATE times in the file
    def filter_user_rate(self,dic):
        users_id = []
        for key in dic :
            if dic[key] >= RATE:
                users_id.append(key)
        return users_id
    #return a list of retweets from a user
    def filter_retweets_from_id(self,user_id):
        list_of_retweets = []
        for retweet in self.retweets:
            if retweet['user']['id'] == int(user_id):
                list_of_retweets.append(retweet)

        return list_of_retweets

    #return a list of retweets that have the same retweeted_status id
    def filter_retweets_RT_id(self,list_of_retweets,RT_id):
        list_of_retweets = []
        for retweet in list_of_retweets:
            if retweet['retweeted_status']['id'] == RT_id:
                list_of_retweets.append(retweet)

        return list_of_retweets


    #check that each one of list_of_userIds follow the author of the original retweet
    #return a list that contains users do not follow the origin author
    def check_followees(self,list_of_userIds):
        users_id = []
        for user_id in list_of_userIds:
            followed = False
            followees_id = getFollowees.getFolloweesFromId(user_id,False)
            for followee_id in followees_id['followees']:
                if(self.origin_author_id == followee_id):
                    followed = True
            if (followed == False):
               print("the user {} does not follow the origin author of retweet where as he appear more than {} in this file, check that.".
                       format(user_id,RATE))
               users_id.appen(user_id)


    def filter_rt_users_of_rate_user(self,save):
        if (save == True):
             rate_users_id = self.rate_users
             for rate_user_id in rate_users_id:
                 list_of_retweets = self.filter_retweets_from_id(rate_user_id)
                 for rt1 in list_of_retweets:
                     rt1_id = rt1['retweeted_status']['id']
                     dic = {}
                     dic['rate_user_id'] = rate_user_id
                     dic['retweeted_id'] = rt1_id
                     dic['retweeted_users'] = []
                     for rt0 in self.retweets:
                         if(rt0['retweeted_status']['id'] == rt1_id ):
                             dic['retweeted_users'].append(rt0['user']['id'])
                     self.write_file(rate_user_id,rt1_id,dic)
        else :
            list_users = []
            rate_users_id = self.rate_users
            for rate_user_id in rate_users_id:
                dic = {}
                dic['rate_user'] = rate_user_id
                dic['retweets_users'] = []
                list_of_retweets = self.filter_retweets_from_id(rate_user_id)
                for rt1 in list_of_retweets:
                    temp_users =[]
                    rt1_id = rt1['retweeted_status']['id']
                    for rt0 in self.retweets:
                        if(rt0['retweeted_status']['id'] == rt1_id ):
                            temp_users.append(rt0['user']['id'])
                    dic['retweets_users'].append(temp_users)
                list_users.append(dic)
            users = []
            for l in list_users:
                d ={}
                d['rate_user'] = l['rate_user']
                for temp in l['retweets_users']:
                    if l['rate_user'] in temp:
                        temp.remove(l['rate_user'])
                    for t in temp:
                        if t in d:
                            d[t] += 1
                        else :
                            d[t] = 1
                users.append(d)
            lol =[]
            for u in users:
                d= {}
                d['rate_user'] = u['rate_user']
                d['children'] = []
                for atr in u:
                      if (u[atr] > 1 and atr != 'rate_user'):
                          d['children'].append(atr)
                lol.append(d)

            for l  in lol :
                for rate_user in self.rate_users:

                    if int(rate_user) in l['children']:
                        l['children'].remove(int(rate_user))

            return lol
           #  for i in range(len(lol)):
           #      print(lol[i])
           #      dic =  getFollowees.getFolloweesFromId(lol[i],False)
           #      for rate_user in self.rate_users:
           #          if('followees' in dic ):
           #              for followee in dic['followees']:
           #                  if(followee == rate_user):
           #                      print('{} follow {}'.format_map(followee,rate_user))




    def build(self):
        list_parent_children = self.filter_rt_users_of_rate_user(False)
        dot = Digraph()
        dot.node('root','DT')
        for parent_children in list_parent_children:
            dot.node(parent_children['rate_user'],parent_children['rate_user'])
            dot.edge('root',parent_children['rate_user'])
            if (len(parent_children['children']) == 0):
                continue
            for child in parent_children['children']:
                dot.node(str(child),str(child))
                dot.edge(parent_children['rate_user'],str(child))
        dot.render('test12345',view=True)



    def write_file(self,user_id,retweet_id,dic):
        folder = self.get_path_to_folder()
        try:
           out_file = open('E/{}/rate_user:{} rt_id: {}'.format(folder,user_id,retweet_id),'w')
        except Exception as e:
            print(e)
            print('Error whiling creating file ')
            exit(0)
        json.dump(dic,out_file,indent=3)
        out_file.close()



    def print_rt(self):
        print(self.retweets)

    def get_path_to_folder(self):
        folder = self.file_name.rsplit('/',1)[0]
        if(folder == self.file_name):
            print('The file must come from samples folder')
            print('Terminating .......')
            exit(0)
        return folder

    def filter(self):
        self.filter_rt_users_of_rate_user(False)

    def check_relation(self,user_id,followee_id,consumer_key,consumer_secret,acc_token,acc_secret):
        author_id = self.retweets['retweeted_status']['user']['id']
        list_of_followees = getFolloweesFromIdTokens(user_id,False,consumer_key,consumer_secret,acc_token,acc_secret)
        for ident in list_of_followees:
            if(ident == followee_id):
                return True
        return False





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filename',help='the file of retweets json file ')
    args = parser.parse_args()
    if(args.filename):
        h = Heuristique3(str(args.filename))
        h.build()

    else:
        print("tape python h3.py --help")
