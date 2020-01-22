# import get_Twitter_Data
#
# twitterData = get_Twitter_Data.TwitterData('2016-04-18')
# api = twitterData.authenticate()
# tweets = twitterData.collectTweets(api, "AAPL", "2018-11-16")

import preprocessTweets
import datetime
from zipfile import ZipFile
from urllib.request import urlopen
from io import StringIO
import csv
import pandas as pd
import os

"""
finds the AFINN score of a word and returns it 
--------------
input: 
    word
    afinn- dictionary contains affin words and its score
--------------    
output:
    total- score
        
"""
# start affin function
def calculateAfinnScore(word, afinn):
    total = 0
    if word in afinn:
        total += afinn[word]
    return total
# end

def main():
    keyword = 'GOOG'
    if keyword == 'GOOG':
        listFiles = os.listdir('data/' + keyword + '/')
        processFiles(listFiles, keyword)


rows_list = []

"""

 function processes each day tweets, pre-processes them
 calculates positive score, negative score, neutral score, hashtags count, total words count  
 fetches the same day historical data for the specific organization and merges it with tweets scores 
 generates csv data
 ----------------
 input:
    listFiles - a list each day tweet files
    keyword - keyword represent a specific organization
 ----------------
 output:
     csv data - positive score, negative score, neutral score, no. of hashtags, no. of words,
     open price, close price, high price, low price, volume of trade
  ---------------
  citation:
     https://github.com/vaibhavmadan96/Twitter-Sentiment-Analysis-and-Stock-prediction/blob/master/ProcessTweets.py
     
"""
def processFiles(listFiles, keyword):

    for file in listFiles:
        filename = 'data/' + keyword + '/' + file
        content_tweets = []

        with open(filename, 'r') as fileHandler:
            content_tweets = fileHandler.read().split("||")
            del content_tweets[len(content_tweets) - 1]

        # print (content_tweets)

        # get stopwords
        stopWords = preprocessTweets.getStopWordList()

        afinn_file = open('./data/AFINN/AFINN-111.txt')

        afinn = dict()
        for line in afinn_file:
            parts = line.strip().split()
            if len(parts) == 2:
                afinn[parts[0]] = int(parts[1])

        # preprocess tweets
        positive_tweet_count = 0
        negative_tweet_count = 0
        neutral_tweet_count = 0
        wordCount = 0
        hashtagCount = 0

        for tweet in content_tweets:
            for tag in tweet.split():
                if tag.startswith("#"):
                    hashtagCount+=1

            tweet = preprocessTweets.processTweet(tweet)
            if len(tweet)==0:
                continue
            # print(tweet)
            words = tweet.split(' ')
            total = 0
            for word in words:
                wordCount += 1
                if word not in stopWords:
                    # print (word)
                    total += calculateAfinnScore(word, afinn)
            # print(total)
            if total > 0:
                positive_tweet_count += 1
            elif total < 0:
                negative_tweet_count += 1
            else:
                neutral_tweet_count += 1

        total_score = positive_tweet_count + negative_tweet_count + neutral_tweet_count
        #print(positive_tweet_count)
        positive_score = str(positive_tweet_count*100/total_score)
        negative_score = str(negative_tweet_count*100/total_score)
        neutral_score = str(neutral_tweet_count*100/total_score)

        extractDate = filename[filename.rfind('/')+1:filename.rfind('.')]
        # extractDate_date = extractDate[extractDate.rfind('-')+1:]
        # extractDate_year = extractDate[0:extractDate.find('-')]
        # extractDate_month = extractDate[extractDate.find('-')+1:extractDate.rfind('-')]
        converted_date = datetime.datetime.strptime(extractDate,'%Y-%m-%d').strftime('%#m/%#d/%Y')
        #print(hashtagCount)

        with open('./data/GOOG.csv') as csv_file:
            next(csv_file)
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == converted_date:
                    # HLPCT = (float(row[2])-float(row[3]))/float(row[3])
                    # print(HLPCT)
                    # PCTchange = (float(row[4])-float(row[1]))/float(row[1])
                    # print(PCTchange)

                    row_List =[round(float(positive_score),2),round(float(negative_score),2),round(float(neutral_score),2),
                              round(float(row[1]),2),round(float(row[5]),2),round(float(row[2]),2),round(float(row[3]),2),
                              row[6],wordCount,hashtagCount]

                    rows_list.append(row_List)
                    break

            generateCSV(rows_list)

"""

Generates a new csv file based on generated csv data
------------
input:
    list of csv data
-----------
output:
    newly generated csv file that contains merged tweets scores and historical data
    each row in csv represents a day of processed data 

"""
def generateCSV(rows_list):

    #print(rows_list)
    tweets_df = pd.DataFrame(rows_list, columns=['positive_score', 'negative_score','neutral_score', 'open_price','close_price','high_price', 'low_price','volume','total_words','total_hashtag'])
    path = './data/newGOOG.csv'
    tweets_df.to_csv(path,index=False)


if __name__ == '__main__':
    main()