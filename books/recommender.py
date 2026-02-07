import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)

#print("base dir" + BASE_DIR)

popular_df = pickle.load(
    open(os.path.join(BASE_DIR, 'popular.pkl'), 'rb')
)
pt = pickle.load(
    open(os.path.join(BASE_DIR, 'pts1.pkl'), 'rb')
)
books2 = pickle.load(
    open(os.path.join(BASE_DIR, 'books1.pkl'), 'rb')
)
similarity_scores = pickle.load(
    open(os.path.join(BASE_DIR, 'similarity_scores1.pkl'), 'rb')
)

def recommend(user_input):
    recommended_data = []

    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        for i in similar_items:
            temp_df = books2[books2['Book-Title'] == pt.index[i[0]]]
            related_book = temp_df.drop_duplicates('Book-Title')['Book-Title'].values
            recommended_data.append(related_book.tolist())

    return recommended_data
