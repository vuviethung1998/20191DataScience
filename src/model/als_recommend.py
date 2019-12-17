import numpy as np
import os

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.recommendation import ALS, ALSModel

conf = SparkConf().setAppName('profile').set('spark.executor.memory', '10g')
spark = SparkSession.builder.config(conf=conf).getOrCreate()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_PATH, "best_model.model")


def loadModel(path):
    model = ALSModel.load(path)
    return model


def recommend(dict):
    model = loadModel(MODEL_PATH)
    iFactor = model.itemFactors.sort(F.col('id'))

    itemKeyF = np.array(iFactor.select(F.col("id")).toPandas()['id'].tolist())

    itemValueF = np.array(iFactor.select(F.col("features")).toPandas()['features'].tolist() )

    full_u = np.zeros(itemKeyF.size)

    for key, val in dict.items():
        set_rating(itemKeyF, full_u, int(key), val)

    recommendations = np.dot(full_u, np.dot(itemValueF,itemValueF.T) )

    top_ten_ratings = np.argpartition(recommendations, -10)[-10:]

    rating = [itemKeyF[rate] for rate in top_ten_ratings]

    return rating


def set_rating(np_keyF, full_u, key, val):
    try:
        idx = list(np_keyF).index(key)
        full_u.itemset(idx, val)
    except:
        idx = list(np_keyF).index(174487)
        full_u.itemset(idx, 4)


# if name == 'main':
#     dict = {
#         "260": 4,
#         "16": 3,
#         "25": 5,
#         "335": 1,
#         "379": 4,
#         "296": 2,
#         "858": 3
#     }
#     top_ten_ratings = recommend(dict)
#     print("Top 10 recommend movie", top_ten_ratings)
