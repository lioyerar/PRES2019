import PyQt5
from ete3 import Tree, TreeStyle, Tree, TextFace, add_face_to_node,faces, AttrFace, NodeStyle
import json
import re

def show(arbre):
    def my_layout(node): #On définit un style pour nos noeuds pour les distinguer dans le rendu
        faces.add_face_to_node(AttrFace("name"), node, column=0, position="branch-right")
        nstyle = NodeStyle()
        if node.is_leaf():
            nstyle["size"] = 15
            nstyle["fgcolor"] = "#ff0000"
            nstyle["vt_line_type"] = 2
            nstyle["hz_line_type"] = 1
            nstyle["vt_line_color"] = "#008000"
            nstyle["hz_line_color"] = "#008000"
        else:
            nstyle["size"] = 30
            nstyle["fgcolor"] = "#0000ff"
            nstyle["vt_line_color"] = "#800000"
            nstyle["hz_line_color"] = "#800000"
        node.set_style(nstyle)
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = my_layout
    ts.mode = "c"
    ts.arc_start = 180
    ts.arc_span = 180
    arbre.show(tree_style=ts)

def drawNames(arbre, name, noms): #prend en arguments un arbre, name : le nom que l'on veut donner à l'image une fois l'arbre tracé, noms : tableaux de correspondance entre id des utilisateurs et leur pseudos
    model = []
    for i in range(len(arbre)-1): #on prépare un tableaux de parenté à partir de l'arbre : arbre. Que l'on a créé au préalable
        tmp = []
        for j in range(len(arbre[i])):
            user = arbre[i][j][1]
            tmp.append(user)
            tmp2 = []
            for k in range(len(arbre[i+1])):
                if(user == arbre[(i+1)][k][0]):
                    tmp2.append(arbre[(i+1)][k][1])
            tmp.append(tmp2)
        model.append(tmp)
    for i in range(len(noms)): #On enlève les caractères spéciaux propres à la synthaxe "newick" pour tracer nos arbres
        noms[i][1] = noms[i][1].replace(',','')
        noms[i][1] = noms[i][1].replace(';','')
        noms[i][1] = noms[i][1].replace('(','')
        noms[i][1] = noms[i][1].replace(')','')
        noms[i][1] = noms[i][1].replace('\\','')
        noms[i][1] = noms[i][1].replace(':','')
        noms[i][1] = noms[i][1].replace(' ','_')
    model.reverse()
    myTrees = []
    for i in range(len(model)): #On transforme chaque éléments de notre arbre de parenté en des arbres qui respectent la synthaxe "newick"
        noeuds = []
        for j in range(0,len(model[i]),2):
            if j%2==0:
                if(model[i][j+1] != []):
                    noeud = "("
                    for k in range(len(model[i][j+1])):
                        if(k != len(model[i][j+1])-1):
                            noeud += str(model[i][j+1][k])+","
                        else:
                            noeud += str(model[i][j+1][k])+")"
                else:
                    noeud=""
                noeud += str(model[i][j])+";"
            if(j%2==0):
                noeuds.append(noeud)
        myTrees.append(noeuds)
    regexp = r"^.*\).*$"
    for i in range(len(myTrees)-1): # On notre des tableau d'arbre newick, on regarder pour chaque éléments i si dans i+1 on a le père pou remplacer et ainsi former un arbre de manière récursive en quelques sortes
        for j in range(len(myTrees[i])):
            tmp = myTrees[i][j]
            tmp = tmp[:-1]
            if re.match(regexp, tmp) is not None:
                analyse = re.sub(r"\((?P<fils>.*)\)(?P<pere>.*)",r"\g<pere>",tmp)
            else:
                analyse = tmp
            taille = len(analyse)
            for k in range(len(myTrees[(i+1)])):
                string = myTrees[(i+1)][k]
                pos = string.find(analyse)
                if(pos != -1):
                    mechant = myTrees[(i+1)][k][pos-1]
                    char = myTrees[(i+1)][k][pos+taille]
                    if(char == ")") or (char == ",") or (char == ";") and (mechant == ")" or mechant == "," or mechant==";" or mechant=="("):
                        myTrees[(i+1)][k] = string.replace(analyse,tmp)
                    else:
                        print("Erreur :"+myTrees[(i+1)][k])
    noms.sort(key=lambda tup: tup[0])
    noms.reverse()
    for i in range(len(noms)): # Dans l'arbre final on remplace les id des utilisateurs par leur pseudo
        myTrees[-1][0] = myTrees[-1][0].replace(str(noms[i][0]), noms[i][1])
    f = open('randomTree.json','w+')
    json.dump(myTrees,f,indent=4)
    A = Tree(myTrees[-1][0],format=8) # Ceci est l'arbre final
    def my_layout(node): #On définit un style pour nos noeuds pour les distinguer dans le rendu
        faces.add_face_to_node(AttrFace("name"), node, column=0, position="branch-right")
        nstyle = NodeStyle()
        if node.is_leaf():
            nstyle["size"] = 15
            nstyle["fgcolor"] = "#ff0000"
            nstyle["vt_line_type"] = 2
            nstyle["hz_line_type"] = 1
            nstyle["vt_line_color"] = "#008000"
            nstyle["hz_line_color"] = "#008000"
        else:
            nstyle["size"] = 30
            nstyle["fgcolor"] = "#0000ff"
            nstyle["vt_line_color"] = "#800000"
            nstyle["hz_line_color"] = "#800000"
        node.set_style(nstyle)
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = my_layout
    ts.mode = "c"
    ts.arc_start = 180
    ts.arc_span = 180
    print("Création d'un rendu dans : Arbre Diffusion "+name+" ...") #On produit un fichier .png représentant l'arbre
    try:
        A.render(name+".png", w=8000, dpi=1000, tree_style=ts)
    except:
        print("Erreur dans "+name)
        pass
    return A

def draw(arbre): #prend en arguments un arbre, name : le nom que l'on veut donner à l'image une fois l'arbre tracé
    model = []
    for i in range(len(arbre)-1): #on prépare un tableaux de parenté à partir de l'arbre : arbre. Que l'on a créé au préalable
        tmp = []
        for j in range(len(arbre[i])):
            user = arbre[i][j][1]
            tmp.append(user)
            tmp2 = []
            for k in range(len(arbre[i+1])):
                if(user == arbre[(i+1)][k][0]):
                    tmp2.append(arbre[(i+1)][k][1])
            tmp.append(tmp2)
        model.append(tmp)
    model.reverse()
    myTrees = []
    for i in range(len(model)): #On transforme chaque éléments de notre arbre de parenté en des arbres qui respectent la synthaxe "newick"
        noeuds = []
        for j in range(0,len(model[i]),2):
            if j%2==0:
                if(model[i][j+1] != []):
                    noeud = "("
                    for k in range(len(model[i][j+1])):
                        if(k != len(model[i][j+1])-1):
                            noeud += str(model[i][j+1][k])+","
                        else:
                            noeud += str(model[i][j+1][k])+")"
                else:
                    noeud=""
                noeud += str(model[i][j])+";"
            if(j%2==0):
                noeuds.append(noeud)
        myTrees.append(noeuds)
    regexp = r"^.*\).*$"
    for i in range(len(myTrees)-1): # On notre des tableau d'arbre newick, on regarder pour chaque éléments i si dans i+1 on a le père pou remplacer et ainsi former un arbre de manière récursive en quelques sortes
        for j in range(len(myTrees[i])):
            tmp = myTrees[i][j]
            tmp = tmp[:-1]
            if re.match(regexp, tmp) is not None:
                analyse = re.sub(r"\((?P<fils>.*)\)(?P<pere>.*)",r"\g<pere>",tmp)
            else:
                analyse = tmp
            taille = len(analyse)
            for k in range(len(myTrees[(i+1)])):
                string = myTrees[(i+1)][k]
                pos = string.find(analyse)
                if(pos != -1):
                    mechant = myTrees[(i+1)][k][pos-1]
                    char = myTrees[(i+1)][k][pos+taille]
                    if(char == ")") or (char == ",") or (char == ";") and (mechant == ")" or mechant == "," or mechant==";" or mechant=="("):
                        myTrees[(i+1)][k] = string.replace(analyse,tmp)
                    else:
                        print("Erreur :"+myTrees[(i+1)][k])
    f = open('randomTree.json','w+')
    json.dump(myTrees,f,indent=4)
    A = Tree(myTrees[-1][0],format=8) # Ceci est l'arbre final
    def my_layout(node): #On définit un style pour nos noeuds pour les distinguer dans le rendu
        faces.add_face_to_node(AttrFace("name"), node, column=0, position="branch-right")
        nstyle = NodeStyle()
        if node.is_leaf():
            nstyle["size"] = 15
            nstyle["fgcolor"] = "#ff0000"
            nstyle["vt_line_type"] = 2
            nstyle["hz_line_type"] = 1
            nstyle["vt_line_color"] = "#008000"
            nstyle["hz_line_color"] = "#008000"
        else:
            nstyle["size"] = 30
            nstyle["fgcolor"] = "#808000"
            nstyle["vt_line_color"] = "#800000"
            nstyle["hz_line_color"] = "#800000"
        node.set_style(nstyle)
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = my_layout
    ts.mode = "c"
    ts.arc_start = 180
    ts.arc_span = 180
    print("Création d'un rendu dans : Arbre Diffusion.png ...") #On produit un fichier .png représentant l'arbre
    try:
        A.render("Arbre Diffusion.png", w=8000, dpi=1000, tree_style=ts)
    except:
        print("Erreur lors de la création de l'arbre")
        pass
    return A
