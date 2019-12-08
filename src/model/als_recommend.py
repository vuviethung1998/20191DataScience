import numpy as np

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.recommendation import ALS, ALSModel

conf = SparkConf().setAppName('profile').set('spark.executor.memory', '10g')
spark = SparkSession.builder.config(conf=conf).getOrCreate()

MODEL_PATH = "src/model/best_model.model"

def loadModel(path):
    model = ALSModel.load(path)
    return model

def recommend(dict):
    model = loadModel(MODEL_PATH)
    iFactor = model.itemFactors

    itemKeyF = iFactor.select(F.col("id")).toPandas()
    itemKeyFToList = itemKeyF['id'].tolist()

    np_keyF = np.array(itemKeyFToList)

    itemValueF = iFactor.select(F.col("features")).toPandas()
    itemValueFToList = itemValueF['features'].tolist()

    np_itemF = np.array(itemValueFToList)

    full_u = np.zeros(np_keyF.size)

    for key, val in dict.items():
        set_rating(np_keyF, full_u, int(key), val)

    recommendations = np.dot(full_u, np.dot(np_itemF, np_itemF.T))

    top_ten_ratings = np.argpartition(recommendations, -10)[-10:]

    return top_ten_ratings

def set_rating(np_keyF, full_u, key, val):
    try:
        idx = list(np_keyF).index(key)
        full_u.itemset(idx, val)
    except:
        pass

if __name__ == '__main__':
    dict = {
        "260": 4,
        "16": 3,
        "25": 5,
        "335": 1,
        "379": 4,
        "296": 2,
        "858": 3
    }
    top_ten_ratings = recommend(dict)
    print("Top 10 recommend movie", top_ten_ratings)