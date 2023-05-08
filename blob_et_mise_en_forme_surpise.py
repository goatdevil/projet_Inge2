
import pandas as pd
import csv
from textblob import TextBlob


with open('df_commentaire_sans_caracteres_speciaux.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    tableau=[]
    compteur=0

    for row in reader:
        compeuruser = 0
        ligne=[]
        for cell in row:
            compeuruser+=1
            if cell=="":
                ligne.append(0)
            else:
                ligne.append(TextBlob(cell).sentiment.polarity)
        #print(ligne)


        if ligne != []:
            ligne.pop(0)
            tableau.append(ligne)
            compteur+=1




f = open("comm_complet2.txt", 'r', encoding='utf-8')

line=f.readline()
liste_hotel=[]
liste_auteur=[]
tableau_text=[]
while line:

    compteur=0
    nom_hotel=""
    nom_auteur=""
    comm=""

    for x in line:
        if x==';':
            compteur+=1
        if compteur==0:
            nom_hotel+=x
        elif compteur==1 and x!=";" :
            nom_auteur+=x
        elif compteur > 1 and x != ";":
            comm += x
    if nom_auteur not in liste_auteur:
        liste_auteur.append(nom_auteur)
    if nom_hotel not in liste_hotel:
        liste_hotel.append(nom_hotel)
    tableau_text.append([nom_hotel,nom_auteur,comm])
    line=f.readline()

df=pd.DataFrame(tableau)
df.index = liste_hotel
df.columns = liste_auteur
df.to_csv("blob.csv")

tab_user=[]
tab_hotel=[]
tab_sentiment=[]
indice_hotel=0
for x in tableau:
    indice_hotel+=1
    indice_user=0
    for sentiment in x:
        indice_user+=1
        if sentiment!=0 :
            tab_user.append(indice_user)
            tab_hotel.append(indice_hotel)
            tab_sentiment.append(sentiment)
df_surprise=pd.DataFrame({"User_id":tab_user,"Hotel_id":tab_hotel,"Sentiment":tab_sentiment})
df_surprise.to_csv("surprise.csv")



