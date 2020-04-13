#%%
import pandas as pd
from fetch_tweets import db_connect

if __name__ == "__main__":
    # Connect with database that stores tweets
    db, cursor = db_connect('data/tweetsDB.db')
    
    sql = '''
    select *
    from tweets
    '''
    df = pd.read_sql(sql, db)

    display(df)
    
    min_date  = min(pd.to_datetime(df['timestamp']).dt.date)
    max_date  = max(pd.to_datetime(df['timestamp']).dt.date)
    print(f'No período: {min_date} a {max_date}')
    
    num_users = len(df['name'].unique())
    print(f'Number of total users: {num_users}')
    print(f'Total Tweets: {df.shape[0]}')
    print(f'Informations obtained : '+', '.join(df.columns.values))

    keywords_list = ['COVID19','Pandemic']
    
    dftemp = df.copy()
    dftemp['text'] = dftemp['text'].apply(lambda x: x.lower())
    for col in keywords_list:
        df[col] = dftemp['text'].str.contains(col.lower())
        sum_col = df[col].sum()
        sum_col_2 = df.groupby('name').agg({col:'count'}).sum()
        print(f'Found {sum_col} tweets for the keyword {col}')
