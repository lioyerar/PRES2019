import json
import sys
import random
import os
import drawTree
import platform
import shutil

def dispTree(arbre): #Pour sauvegarder notre arbre dans un fichier .txt
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

def getTweets(elt): #On récupère tout les tweets DIFFERENTS du fichier de capture
    taille = len(elt)
    tweets = []
    for i in range(taille):
        tmp = elt[i]
        if('id' in tmp['retweeted_status']) and (tmp['retweeted_status']['id'] not in tweets):
            tweets.append(tmp['retweeted_status']['id'])
    return tweets

def getUsersByTweets(tweets, contenu): #On produit un tableau qui, pour chaque tweet donne les utilisateurs qui ont retweeté
    eachTweets = []
    nomParTweet = []
    for i in range(len(tweets)):
        tweet = tweets[i]
        actual = []
        noms = []
        for j in range(len(contenu)):
            tmp = contenu[j]
            if (tmp['retweeted_status']['id'] == tweet):
                if ('id' in tmp['user']):
                    if (tmp['user']['id'] not in actual):
                        actual.append(tmp['user']['id'])
                        if('name' in tmp['user']):
                            if (tmp['user']['name'] not in actual):
                                str = tmp['user']['name']
                                noms.append([tmp['user']['id'], str])
        eachTweets.append(actual)
        nomParTweet.append(noms)
    res = []
    res2 = []
    for i in range(len(eachTweets)):
        if(len(eachTweets[i]) > 10) :#and (len(eachTweets[i]) < 50): #Décommentez la fin de la condition pour créer des arbre de taille limitée
            res.append((tweets[i], eachTweets[i]))
            res2.append((tweets[i], nomParTweet[i]))
    return (res,res2) #On renvoie le tableau mais également un tableau de correspondance entre id utilisateurs et pseudos utilisateurs

def build(data): #On construit un arbre aléatoire à partir des utilisateurs pour chaque tweet
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
            tmp.sort(key=lambda tup: tup[0])
            arbre.append(tmp)
            for i in range(len(tmp)):
                users.remove(tmp[i][1])
            j += 1
    return arbre

def writting(arbre): #On colle notre arbre dans un fichier .json si jamais on veut garder une trace réutilisable
    f = open('randomTree.json','w+')
    json.dump(arbre,f,indent=4)

if __name__== '__main__':
    if(len(sys.argv) < 2):
        print("Usage : python randomTree.py <nom fichier retweets>.txt")
    else:
        f1 = open(sys.argv[1])
        contenu = f1.read()
        elt = json.loads(contenu.strip())
        tweets = getTweets(elt)
        data, data2 = getUsersByTweets(tweets, elt)
        arbre = []
        for i in range(len(data)):
            arbre.append(build(data[i]))
        OS = platform.system()
        if(OS == "Windows"): #On créer un dossier dans lequel on va mettre nos fichier .png de rendu pour les avoir dans le répertoire racine
            path = "rendus\\"
        else:
            path = "rendus/"
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        print(str(len(data))+" rendus en attente :")
        for i in range(len(arbre)): #On produit un rendu pour tout les tweets
            print("("+str(i+1)+"/"+str(len(data))+")")
            tree = drawTree.drawNames(arbre[i],path+"Arbre Diffusion "+str(i+1),data2[i][1])
        #drawTree.show(tree)
