import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from surprise import Reader
from surprise import Dataset
from surprise import SVD
from surprise import SVDpp
from surprise import NMF
from surprise.model_selection.search import GridSearchCV

from surprise.model_selection import cross_validate
import random


reader=Reader(rating_scale=(-1,1))

df=pd.read_csv("surprise.csv")
df2=pd.read_csv("blob.csv")
column=list(df2.columns)
column.pop(0)

#création des dictionnaire nom_user => id_user et id_hotel=>nom_hotel
dico_user={}
compteur=0
for user in column:
    compteur+=1
    dico_user[user]=compteur

liste_hotel=list(df2["Unnamed: 0"].values)
dico_hotel={}
compteur=0
for hotel in liste_hotel:
    compteur+=1
    dico_hotel[compteur]=hotel




#data=Dataset.load_from_file("surprise.csv",reader)
data=Dataset.load_from_df(df[["User_id","Hotel_id","Sentiment"]],reader)
svd = SVD(verbose=True, n_epochs=10)
cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=9, verbose=True)
nmf = NMF(verbose=True, n_epochs=10)
cross_validate(nmf, data, measures=['RMSE', 'MAE'], cv=9, verbose=True)
svdpp=SVDpp(verbose=True, n_epochs=10)
cross_validate(svdpp, data, measures=['RMSE', 'MAE'], cv=9, verbose=True) # calcul RMSE et MAE pour les modeles SVD et SVD++

trainset=data.build_full_trainset() #création du dataset de training

grid={'n_epochs': [8,9,10,11,12,13,14,15, 20],
        'lr_all': [.0025, .005,.0075, .001,.005, .01]}

gs = GridSearchCV(SVDpp, grid,measures=['RMSE','MAE'], cv=9)
gs.fit(data)
param=gs.best_params['rmse']
svdpp=SVDpp(verbose=True, n_epochs=param['n_epochs'],lr_all=param['lr_all'])


svdpp.fit(trainset)# choix de SVD++ car RMSE et MAE moyen plus faible



len_hotelid=max(df["Hotel_id"])
len_userid=max(df["User_id"])



def predict_review(user_id, hotel_id, model):

    review_prediction = model.predict(uid=user_id, iid=hotel_id)
    return review_prediction.est


def generate_recommendation(nom_user, model, metadata, thresh=0.45):#generation des recommendation avec sauvegarde si score predi>0,45
    user_id=dico_user[nom_user]
    recommended_hotel=[]
    hotel_ids = list(metadata['Hotel_id'].values)
    hotel_comm=df[df["User_id"]==user_id][["Hotel_id"]]
    hotel_comm=list(hotel_comm["Hotel_id"].values)
    random.shuffle(hotel_ids)

    for hotel_id in hotel_ids:
        rating = predict_review(user_id, hotel_id, model) # prédit une note de commentaire théorique
        if rating >= thresh: #si score >0,45 on sauvegarde l'id de l'hotel
            recommended_hotel.append(hotel_id)

    return hotel_comm,set(recommended_hotel)

hotel_comm,hotel_reco=generate_recommendation(" James R",svdpp,df)
nom_hotel_comm=[]
for indice in hotel_comm: #On utilise le dictionnaire id_hotel=> nom_hotel pour afficher le nom des hotels ou la personne à laisser un commentaire
    nom_hotel_comm.append(dico_hotel[indice])
print(nom_hotel_comm)

nom_hotel_reco=[]
for indice in hotel_reco:#Pareil pour les hotels que l'on recommande
    nom_hotel_reco.append(dico_hotel[indice])
print(nom_hotel_reco)
