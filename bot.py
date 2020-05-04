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

# serach for covid
text1 = 'coronavirus'
text2 = 'covid'
text3 = 'lockdown'
text4 = 'pandemia'

# read file
df = pd.read_csv('account.csv')


# for each csv row 
for index, row in df.iterrows():
    
    # take data
    account = row['Account']
    last_tweet_id = row['LastTweetID']
    
    # tweet number limit
    max_tweets = 100
    
    # take all user tweets
    searched_tweets = [status.id for status in 
                       tweepy.Cursor(api.user_timeline, id = account, since_id = last_tweet_id,
                                     exclude_replies = True).items(max_tweets)]
    
    # cycle
    for idx, i in enumerate(searched_tweets):
        tweet = api.get_status(i, tweet_mode = 'extended')  # all the text
        tweetText = tweet.full_text   # take text
        tweetText = tweetText.lower()   # lowercase
        if idx == 0: df.iloc[index,3] = tweet.id   # last retweeted id
        # filter only covid tweets and exclude retweets
        if not(tweetText.startswith('rt')) and (tweetText.find(text1) + 
                                                tweetText.find(text2) + 
                                                tweetText.find(text3) + 
                                                tweetText.find(text4)) > -4:
                # tweet!
                api.retweet(i)

# write output with last tweet
df.to_csv('account.csv', index=False)







