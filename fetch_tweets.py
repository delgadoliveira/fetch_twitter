# %%
import time
import tweepy
import sqlite3
import pandas as pd

def twitter_credentials(
    consumer_key, 
    consumer_key_secret,
    access_token,
    access_token_secret):

    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return auth, api

def get_current_max_id(cursor):
    max_id = 0
    
    try:
        sql = '''
            SELECT MAX(tweet_id)
            FROM Tweets
        '''

        cursor.execute(sql)
        max_id = cursor.fetchone()[0]
    
    finally:
        return max_id

def db_connect(path_db):
    db = sqlite3.connect(path_db)
    cursor = db.cursor()
    
    return db, cursor

def create_tweets_table(db, db_cursor):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS 
                Tweets(
                id INTEGER PRIMARY KEY,
                tweet_id INTEGER,
                name TEXT, 
                geo TEXT, 
                image TEXT, 
                source TEXT, 
                timestamp TEXT, 
                text TEXT, 
                rt INTEGER)'''

        db_cursor.execute(sql)
        db.commit()
         
        return True

    except:
        return False

def check_if_tweet_exists(db, tweet):
    sql = '''
    SELECT tweet_id
    from Tweets
    '''

    list_tweets_id = pd.read_sql(sql, db).values
    if tweet.id in list_tweets_id:
        return True
    
    return False

def insert_tweet(db, db_cursor, tweet):
    if check_if_tweet_exists(db, tweet):
        return True

    try:
        sql = f'''INSERT INTO Tweets(
        tweet_id, 
        name, 
        geo, 
        image, 
        source, 
        timestamp, 
        text, 
        rt) 
        VALUES(
        {tweet.id},
        "{tweet.user.screen_name}",
        "{tweet.geo}",
        "{tweet.user.profile_image_url}",
        "{tweet.source}",
        "{tweet.created_at}",
        '{tweet.full_text}',
        {tweet.retweet_count})'''

        db_cursor.execute(sql)
    finally:
        return True
    # except sqlite3.Error as e:
    #     print(type(e).__name__)
    #     return False

def fetch_tweets(
    api,
    query,
    max_tweets=50000,
    use_since_id=False,
):

    since_id=0

    if use_since_id:
        since_id = get_current_max_id(cursor)
        
    c = tweepy.Cursor(api.search,
                q=query,
                include_entities=True,
                wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True,
                retry_delay = 3600,
                retry_count = 100,
                since_id = since_id,
                result_type='recent',
                tweet_mode='extended',
                lang="pt").items(max_tweets)

    return c

if __name__ == "__main__":

    #Twitter Developer keys here
    consumer_key = ''
    consumer_key_secret = ''
    access_token = ''
    access_token_secret = ''

    # Connect with database that stores tweets
    db, cursor = db_connect('data/tweetsDB.db')

    # Create table Tweets
    assert create_tweets_table(db, cursor)

    #Authenticate using Tweepy
    auth, api = twitter_credentials(
        consumer_key,
        consumer_key_secret,
        access_token,
        access_token_secret
    )

    query = '''
           COVID19
           OR pandemic
        '''

    tweetCount = 0 
    max_tweets = 100000

    #Fetch tweets    
    c = fetch_tweets(
        api, 
        query, 
         max_tweets = 100000,
        use_since_id=False)
        
    while True:
        try:
            tweet = c.next()
            assert insert_tweet(db, cursor, tweet)
            db.commit()
            tweetCount += 1
        except tweepy.TweepError as e:
            print("In the except method")
            print(e.reason)
            time.sleep(60 * 15)
        except StopIteration:
            print(f'Downloaded {tweetCount} tweets.')
            break

    cursor.close()
    db.close()
