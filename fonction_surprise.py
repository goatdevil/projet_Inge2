from surprise import SVDpp
from surprise import Reader
from surprise import Dataset
from surprise.model_selection.search import GridSearchCV
import pandas as pd
import random
from textblob import TextBlob
import csv

reader = Reader(rating_scale=(-1, 1))
df = pd.read_csv("surprise.csv")
df2 = pd.read_csv("blob.csv")
df3=pd.read_csv("df_commentaire.csv")
dico_user_id = {}
dico_id_user = {}
compteur = 0

column = list(df2.columns)
column.pop(0)

for user in column:
    compteur += 1
    dico_user_id[user] = compteur
    dico_id_user[compteur] = user

liste_hotel = list(df2["Unnamed: 0"].values)
dico_hotel_id = {}
dico_id_hotel = {}
compteur = 0
for hotel in liste_hotel:
    compteur += 1
    dico_id_hotel[compteur] = hotel
    dico_hotel_id[hotel] = compteur


def création_fit_model(df):
    data = Dataset.load_from_df(df[["User_id", "Hotel_id", "Sentiment"]], reader)
    trainset = data.build_full_trainset()

    grid = {'n_epochs': [8, 9, 10, 11, 12, 13, 14, 15, 20],
            'lr_all': [.0025, .005, .0075, .001, .005, .01]}

    gs = GridSearchCV(SVDpp, grid, measures=['RMSE', 'MAE'], cv=9)
    gs.fit(data)
    param = gs.best_params['rmse']
    svdpp = SVDpp(verbose=True, n_epochs=param['n_epochs'], lr_all=param['lr_all'])
    svdpp.fit(trainset)
    return svdpp


def refit(df, new_df, model):
    df = pd.concat([df, new_df])
    new_data = Dataset.load_from_df(df[["User_id", "Hotel_id", "Sentiment"]], reader)
    new_trainset = new_data.build_full_trainset()
    model.fit(new_trainset)
    return model, df


def predict_review(user_id, hotel_id, model):
    review_prediction = model.predict(uid=user_id, iid=hotel_id)
    return review_prediction.est


def generate_recommendation(nom_user, model, metadata,thresh=0.45):  # generation des recommendation avec sauvegarde si score predi>0,45
    user_id = dico_user_id[nom_user]
    recommended_hotel = []
    hotel_ids = list(metadata['Hotel_id'].values)
    hotel_comm = df[df["User_id"] == user_id][["Hotel_id"]]
    hotel_comm = list(hotel_comm["Hotel_id"].values)
    random.shuffle(hotel_ids)

    for hotel_id in hotel_ids:
        rating = predict_review(user_id, hotel_id, model)  # prédit une note de commentaire théorique
        if rating >= thresh:  # si score >0,45 on sauvegarde l'id de l'hotel
            recommended_hotel.append(hotel_id)

    return hotel_comm, set(recommended_hotel)


def affichage_recommendation(hotel_comm, hotel_reco):
    nom_hotel_comm = []
    for indice in hotel_comm:  # On utilise le dictionnaire id_hotel=> nom_hotel pour afficher le nom des hotels ou la personne à laisser un commentaire
        nom_hotel_comm.append(dico_id_hotel[indice])
    print(nom_hotel_comm)

    nom_hotel_reco = []
    for indice in hotel_reco:  # Pareil pour les hotels que l'on recommande
        nom_hotel_reco.append(dico_id_hotel[indice])
    print(nom_hotel_reco)
    return


def ajout_new_comm(newdf,nom_user, nom_hotel,comm,df_text=df3):
    id_user = dico_user_id[nom_user]
    id_hotel = dico_id_hotel[nom_hotel]
    ajout_df = pd.DataFrame(
        {"User_id": [id_user], "Hotel_id": [id_hotel], "Sentiment": [TextBlob(comm).sentiment.polarity]})
    df_text.at[id_hotel+1,nom_user]=comm
    newdf = pd.concat(newdf, ajout_df)
    return newdf,df_text


def find_comm(nom_user):
    id_user = dico_user_id[nom_user]
    tab_comm = []
    with open('df_commentaire_sans_caracteres_speciaux.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        row = reader[id_user]
        for comm in row:
            if comm != "":
                tab_comm.append(comm)
    return tab_comm


