import pandas as pd
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
liste_hotels_tableau=[]
compteur_hotel=0

compteur_user=0


for x in liste_hotel:
    liste_hotels_tableau.append("")
for indice_h in range(len(liste_hotel)):
    compteur_hotel+=1
    print(compteur_hotel)
    liste_users = []
    for x in liste_auteur:
        liste_users.append("")

    for indice_u in range(len(liste_auteur)):
        compteur_user+=1
        for indice_text in range(len(tableau_text)):

                text=tableau_text[indice_text]
                if text[1] == liste_auteur[indice_u] and text[0]==liste_hotel[indice_h]:
                    liste_users[indice_u] = text[2]
    print(len(liste_users))
    print(len(liste_hotels_tableau))





   liste_hotels_tableau[indice_h]=liste_users


df=pd.DataFrame(liste_hotels_tableau)

df.columns = liste_auteur
df.index = liste_hotel
df.to_csv("df_commentaire.csv")


