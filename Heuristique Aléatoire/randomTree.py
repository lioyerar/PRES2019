import json
import sys
import random

def dispTree(arbre):
    output = ""
    for i in range(len(arbre)):
        output += ("étage"+str(i)+"\n[")
        for j in range(len(arbre[i])):
            output += str(arbre[i][j])
            if(j != len(arbre[i])-1):
                output += ", "
        output += "]\n\n"
    f = open('randomTree.txt','w+')
    f.write(output)
    print("L\'arbre de diffusion aléatoire est dans \"randomTree.txt\"")

def getTweets(elt):
    taille = len(elt)
    print("Nombre de retweets capturés :",taille)
    tweets = []
    for i in range(taille):
        tmp = elt[i]
        if('id' in tmp['retweeted_status']) and (tmp['retweeted_status']['id'] not in tweets):
            tweets.append(tmp['retweeted_status']['id'])
    print("Nombre de tweets différents dans la capture :",len(tweets))
    return tweets

def getUsersByTweets(tweets, contenu):
    eachTweets = []
    for i in range(len(tweets)):
        tweet = tweets[i]
        actual = []
        for j in range(len(contenu)):
            tmp = contenu[j]
            if (tmp['retweeted_status']['id'] == tweet):
                if ('id' in tmp['user']):
                    if (tmp['user']['id'] not in actual):
                        actual.append(tmp['user']['id'])
        eachTweets.append(actual)
    res = []
    for i in range(len(eachTweets)):
        if(len(eachTweets[i]) > 10):
            res.append((tweets[i], eachTweets[i]))
    return res

def build(data):
    id = data[0]
    users = data[1]
    users.sort()
    arbre = [[(id,id)]]
    j = 0
    while users != []:
        tmp = []
        for i in range(len(users)):
            bool = random.random()
            if bool > 0.5:
                bool2 = random.random() * len(arbre[j])
                bool2 = int(bool2)
                tmp.append((arbre[j][bool2][1],users[i]))
        if tmp != []:
            tmp.sort(key=lambda tup: tup[1])
            arbre.append(tmp)
            for i in range(len(tmp)):
                users.remove(tmp[i][1])
            j += 1
    return arbre

def writting(arbre):
    f = open('randomTree.json','w+')
    json.dump(arbre,f,indent=4)
    print("L\'arbre de diffusion aléatoire est dans \"randomTree.json\"")

if __name__== '__main__':
    if(len(sys.argv) < 2):
        print("Usage : python randomTree.py <nom fichier retweets>.txt")
    else:
        f1 = open(sys.argv[1])
        contenu = f1.read()
        elt = json.loads(contenu.strip())
        tweets = getTweets(elt)
        data = getUsersByTweets(tweets, elt)
        arbre = build(data[0])
        dispTree(arbre)
        writting(arbre)
