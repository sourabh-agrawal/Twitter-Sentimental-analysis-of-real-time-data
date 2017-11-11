import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = "Enter your consumer key here"
        consumer_secret = "Enter your consumer_secret key here"
        access_token = "Enter your access_token key here"
        access_token_secret = "Enter your access_token_secret key here"
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)

            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)

            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):

        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''

        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(?:\@|https?\:\/\/)\S+", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):

        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))

        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 200):

        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:

            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:

                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                #self.clean_tweet(tweet.text)
                parsed_tweet['text'] = self.clean_tweet(tweet.text)

                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:

                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)

            print("Error : " + str(e))
def bar (p,ne,nu):
    objects = ('Positive', 'negative', 'neutral')
    y_pos = np.arange(len(objects))
    performance = [int(p),int(ne),int(nu)]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('No of tweets')
    plt.xlabel('Type of tweet')
    plt.title('Twitter sentimental analysis')
    plt.show()
def pie(p,ne,nu):

    # Data to plot
    labels = 'Positive', 'negative', 'neutral'
    total = int(p) + int(ne) +int(nu)
    sizes = [int(p)/total, int(ne)/total, int(nu)/total]
    colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0)  # explode 1st slice
     
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
     
    plt.axis('equal')
    plt.show()
def main():
    # creating object of TwitterClient Class

    api = TwitterClient()
    topic = input("what you want to search? :\t")

    # calling function to get tweets
    tweets = api.get_tweets(query = topic, count = 200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    
    print("\nNo of total tweets: ",len(tweets))
    print("no of positive tweets: ",len(ptweets))
    print("no of negative tweets: ",len(ntweets))
    print("no of neutral tweets: ",(len(tweets)-len(ntweets)-len(ptweets)))
    

    # percentage of positive tweets
    print("\nPositive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

    count = 1
    while (count != -1):
        x = int(input("\n\nFor positive tweets press 1\nFor negative tweets press 2\nFor neutral tweets press 3\nFor bar chart press 4\nFor pie chart press 5\n \t:"))
        if x == 1:

            # printing first 5 positive tweets
            print("\n\nPositive tweets:\n")
            for tweet in ptweets:
                print(tweet['text'])
            count = int(input("\n\npress -1 for exit \t press any no for repeat\n:"))
        elif x == 2:

            # printing first 5 negative tweets
            print("\n\nNegative tweets:\n")

            #for tweet in ntweets[:10]:
            for tweet in ntweets:
                print(tweet['text'])
            count = int(input("\n\npress -1 for exit \t press any no for repeat\n:"))
        elif x == 3:

            # printing first 5 neutral tweets
            print("\n\nNeutral tweets:\n")
            for tweet in tweets:
                if tweet not in ptweets:
                    if tweet not in ntweets:
                        print(tweet['text'])        
            count = int(input("\n\npress -1 for exit \t press any no for repeat\n:"))
        elif x ==4:
            positive = len(ptweets)
            negative = len(ntweets)
            neutral = len(tweets) - len(ptweets) - len(ntweets)
            bar(positive,negative,neutral)
            count = int(input("\n\npress -1 for exit \t press any no for repeat\n:"))
        elif x ==5:
            positive = len(ptweets)
            negative = len(ntweets)
            neutral = len(tweets) - len(ptweets) - len(ntweets)
            pie(positive,negative,neutral)
            count = int(input("\n\npress -1 for exit \t press any no for repeat\n:"))
if __name__ == "__main__":

    # calling main function
    main()
