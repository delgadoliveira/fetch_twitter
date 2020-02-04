#%%
import tweepy


#Twitter Developer keys here
consumer_key = 'TNGWkCawmMuagFbwVPIyHLtG9'
consumer_key_secret = 'OlsaM7gIqyNx5CVvcLIZl94HEKaqFfO8vSsK8GpbFN94klhj7Y'
access_token = '64504545-BnAbV1rakijSvTKT9MZRu8Vv9AVKdfdYNZWqqnHRM'
access_token_secret = 'ihgPozL7gFiO2R26HHUDsm4RYdGvL83j1mDDnmqLOO3hZ'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")