import joblib
import pandas as pd

model_mapping = {
    "0" : "c0.sav",
    "1" : "c1.sav",
    "2" : "c2.sav",
    "3" : "c3.sav",
    "4" : "c4.sav",
    "5" : "c5.sav"   
}

def predict(prod,weeks):

    global model_mapping

    dataDF = (
	    pd.read_csv('data/product_mapping.csv')
    )
    cluster = dataDF[dataDF['product_number']==prod]['km_cluster'].item()
    cluster_file = model_mapping[f'{cluster}'] 
    clf = joblib.load(f'data/{cluster_file}')
    forecast = clf.predict(weeks)
    print(forecast)
    return forecast

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