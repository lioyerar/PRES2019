#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:23:42 2019

@author: root
"""
import simplejson as json
from tweet_parser.tweet import Tweet
from tweet_parser.tweet_parser_errors import NotATweetError
import fileinput

def filterTweetID():
    for line in fileinput.FileInput("test.txt" ):
        try:
            tweet_dict = json.loads(line)
            tweet = Tweet(tweet_dict)
        except (json.JSONDecodeError,NotATweetError):
            pass
        print(tweet.created_at_string, tweet.all_text)



def filterTweetIDv2(filename):
    i=1
    try:
        file = open(filename,'r')
        line = file.readline()
        result=[]
        outFile = open('output.txt','w')
        id = 996790273576497153
    
    except:
        print(filename+' does not exist')
        exit(0)
        
    while(line and i<100000000  ):   
        try:
            dict = {}
            dict['created_at'] = None
            dict['id'] = None
            dict['text'] = None
            dict['user'] = {}
            dict['retweeted_status'] = {}
            tweet = json.loads(line.strip())
            if 'text' in tweet:
                if(tweet['retweeted_status']['id']==id):
                    dict['created_at']=tweet['created_at']
                    dict['id'] = tweet['id']
                    dict['user']['id'] = tweet['user']['id']
                    dict['retweeted_status']['id'] = tweet['retweeted_status']['id']
                    dict['text'] = tweet['text']
                    print(dict)
                    result.append(dict)
                    
        except json.JSONDecodeError:
            print('line '+str(i)+', incorrect json format')  
        
        except:
            print('unknow error at line: ',i)
            print(line)
        
        finally:
            print('____________________________________________________________________')
            i = i +1
            line = file.readline()

    json.dump(result,outFile,indent=4)
    
    
    
    
    
    
if __name__== '__main__':
    file = open('test.txt','r')
    filterTweetIDv2('test.txt')
    #filterTweetID()
    
    