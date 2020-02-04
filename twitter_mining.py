import tweepy
from tweepy import OAuthHandler
import jsonpickle

# Define keys, secrets and API object
consumer_key = 'TNGWkCawmMuagFbwVPIyHLtG9'
consumer_secret = 'OlsaM7gIqyNx5CVvcLIZl94HEKaqFfO8vSsK8GpbFN94klhj7Y'
access_token = '64504545-hzGLkpWXZN4o7nbSG0pPACR4AKbM14tIt6V0gSLwc'
access_token_secret = 'Tjz4Z1jvObXsyIhk4cuqklTNzWZ8tSkdKHs1ebUw3aXPh'
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define function to save tweets
def get_save_tweets(filepath, api, query, max_tweets=50000, lang='pt', sinceId=0, maxId=99999999999999999999):
    tweetCount = 0
    max_id = 0

    #Open file and save tweets
    with open(filepath, 'w') as f:

        # Send the query
        #Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD. 
        #Keep in mind that the search index has a 7-day limit. 
        #In other words, no tweets will be found for a date older than one week.
        for tweet in tweepy.Cursor(api.search,
                                   q=query,
                                   since_id=sinceId,
                                   max_id=maxId,
                                   lang=lang,
                                   result_type='recent',
                                   include_entities=True,
                                   exclude_replies = True,
                                   tweet_mode='extended').items(max_tweets):         

                max_id = max(max_id, int(tweet._json['id']))
                #Convert to JSON format
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
                tweetCount += 1

    #Display how many tweets we have collected
    print(f'Downloaded {tweetCount} tweets. Max Id = {max_id}')

    return max_id

# Define query
query = 'keyword1 OR keyword2'

# Mine tweets
i = 0
max_id = 0
while True:
        max_id = get_save_tweets(f'tweets_amazon_{i}.json', api, query, sinceId=max_id)
