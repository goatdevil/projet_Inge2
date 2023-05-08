
import numpy as np

f=open('test4.txt','r',encoding='utf_8')
f3=open('test4.txt','r',encoding='utf_8')
f2=open('comm2_0.txt','a',encoding='utf-8')
f4=open('test4_sansdoublon.txt',"a",encoding='utf-8')
line=f.readline()
compteur=0
listenom=[]
liste_indice_doublon=[]
while line:

    compteur_mot=0
    nom=""
    for x in line:


        if x ==",":
            compteur_mot+=1
        elif compteur_mot==1 :
            nom+=x
    listenom.append(nom)
    line = f.readline()


for y in range(len(listenom)):
    compteur_premier=0
    for x in range(y+1,len(listenom)):
            compteur_premier+=1
            try:
                   if listenom[x]==listenom[y]:
                       if y not in liste_indice_doublon:
                            liste_indice_doublon.append(y)
                       liste_indice_doublon.append(x)

            except: None

liste_indice_doublon[:]=np.unique(liste_indice_doublon)
for x in range(len(listenom)):
    ligne = f3.readline()
    if x in liste_indice_doublon:
        f2.write(ligne)





