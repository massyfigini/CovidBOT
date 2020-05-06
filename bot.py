"""
Created on Fri May 01 2020

@author: massyfigini
"""

C_KEY = "*******************"  
C_SECRET = "**************************************************"  
A_TOKEN = "***************************************************"  
A_TOKEN_SECRET = "********************************************"  

#pip install tweepy

# import libraries
import tweepy
import pandas as pd

# Authenticate to Twitter
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

# serch for covid
text1 = 'coronavirus'
text2 = 'covid'
text3 = 'lockdown'
text4 = 'pandemia'

text = [text1, text2, text3, text4]

# read file
df = pd.read_csv('account.csv')


# for each row of my csv
for index, row in df.iterrows():
    
    # take data
    account = row['Account']
    last_tweet_id = row['LastTweetID']
    
    # tweet limit
    max_tweets = 1000
    
    # take all user tweets
    searched_tweets = [status.id for status in 
                       tweepy.Cursor(api.user_timeline, id = account, since_id = last_tweet_id,
                                     exclude_replies = True).items(max_tweets)]
    
    # for each tweet
    for idx, i in enumerate(searched_tweets):
        tweet = api.get_status(i, tweet_mode = 'extended')  # all the text
        tweetText = tweet.full_text   # take text
        tweetText = tweetText.lower()   # lowercase
        if idx == 0: df.iloc[index,3] = tweet.id   # last retweeted id
        # filter only covid tweets and exclude retweets
        if not(tweetText.startswith('rt')) and any(x in tweetText for x in text):
            # tweet!    
            api.retweet(i)

# rewrite account.csv with last id tweet updated
df.to_csv('account.csv', index=False)
