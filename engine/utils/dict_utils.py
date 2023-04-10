import pandas as pd
def Df_to_Dict(row,index,index_key,keys):
    df_to_dict = {}
    if index and index_key:
        df_to_dict = {
            index_key: index
        }
    for key in keys:
        df_to_dict[key] = row[key] if not pd.isna(row[key]) else None
    return df_to_dict

def get_future_days_stock():
    import datetime
    t = datetime.datetime.today()
    future = datetime.datetime(t.year,t.month,t.day,7,0)
    if t.hour >= 7:
        future += datetime.timedelta(days=1)
    return future,t
