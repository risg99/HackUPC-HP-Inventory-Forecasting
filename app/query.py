import joblib
import pandas as pd
import numpy as np
import datetime

model_mapping = {
    "0" : "c0",
    "1" : "c1",
    "2" : "c2",
    "3" : "c3",
    "4" : "c4",
    "5" : "c5"   
}

def predict(prod,weeks):

    global model_mapping

    dataDF = (
	    pd.read_csv('data/product_mapping.csv')
    )
    cluster = dataDF[dataDF['product_number']==prod]['gmm_cluster'].item()
    cluster_file = model_mapping[f'{cluster}'] 

    clf = joblib.load(f'data/{cluster_file}.sav')
    clf_sale = joblib.load(f'data/{cluster_file}_sale.sav')

    clusterDF = (
	    pd.read_csv('data/cluster_details.csv')
    )
    fc = clf.predict(weeks)
    fc = fc.to_frame().rename(columns = {0: 'forecast'}).reset_index().rename(columns = {'index': 'date'})

    fc['forecast_cumsum'] = fc['forecast'].cumsum()
    fc['first'] = fc['forecast_cumsum']+ clusterDF[clusterDF['cluster']==cluster]['last_diff'].item()
    fc['first_cumsum'] = fc['first'].cumsum()
    fc['second'] = fc['first_cumsum']+ clusterDF[clusterDF['cluster']==cluster]['last_train'].item()
    fc['second'] = np.exp(fc[['second']]) - 1
    fc.rename(columns = {'second': 'inventory_units'}, inplace = True)

    sales_clusterDF = (
	    pd.read_csv('data/sales_cluster_details.csv')
    )
    fc_sale = clf_sale.predict(weeks)
    fc_sale = fc_sale.to_frame().rename(columns = {0: 'forecast'}).reset_index().rename(columns = {'index': 'date'})

    fc_sale['forecast_cumsum'] = fc['forecast'].cumsum()
    fc_sale['first'] = fc_sale['forecast_cumsum']+ sales_clusterDF[sales_clusterDF['cluster']==cluster]['last_diff'].item()
    fc_sale['first_cumsum'] = fc_sale['first'].cumsum()
    fc_sale['second'] = fc_sale['first_cumsum']+ sales_clusterDF[sales_clusterDF['cluster']==cluster]['last_train'].item()
    fc_sale['second'] = np.exp(fc_sale[['second']]) - 1
    fc_sale.rename(columns = {'second': 'sales_units'}, inplace = True)

    fullDF = (
	    pd.read_csv('data/product_data.csv')
    )
    fc['product_number'] = prod
    fc = fc.merge(fullDF[fullDF['product_number']== prod],how='left' )
    fc['year_week'] = fc.apply(lambda x: x['date'].year * 100 + int(x.date.isocalendar()[1]), axis = 1)
    fc['sales_units'] = fc_sale['sales_units']
    print(fc)
    return fc

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