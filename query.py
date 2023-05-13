import joblib
import pandas as pd

def predict():

    ## sample
    clf = joblib.load('model.pkl')
    probabilities = clf.predict_proba('X')
    return probabilities

def get_history():
    dataDF = (
	    pd.read_csv('data/preprocessed_train.csv')
    )
    return dataDF

def get_hp_data():

    dataDF = (
	    pd.read_csv('data/preprocessed_train.csv')
    )

    products = dataDF["product_number"].sort_values().unique()
    segments = dataDF["segment"].sort_values().unique()
    productCategories = dataDF["prod_category"].sort_values().unique()
    dates = dataDF['date']

    return products, segments, productCategories, dates