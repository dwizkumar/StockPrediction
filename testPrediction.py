from getTwitterData import TwitterData
from getFinanceData import financeData
from modelBuilding import ModelBuild
from nltk.stem import PorterStemmer
import datetime
import preprocessTweets
import pandas as pd

"""
    test_predict function fetches real-time tweets, pre-processes them,
    runs porters algorithms for stemming, calculates sentiment scores, 
    fetches real-time historical data using Yahoo! finance API, 
    merges both tweets score and historical data, uses built models
    to predict outcome.
    ------------
    input: 
        company name
    ------------    
    output:     
        predicted results, test feature list, sentiment scores
"""
class PredictData:

    def test_predict(self, comp_name):

        today = datetime.datetime.now()
        today = today.strftime("%Y-%m-%d")
        keyword = comp_name

        #twitterData = getTwitterData.TwitterData('2016-04-18')
        twitterData = TwitterData()
        api = twitterData.authenticate()
        # print(api)

        porter = PorterStemmer()

        tweets = twitterData.getTweets(api, keyword, today)
        print(tweets)

        # start affin function
        def calculateAfinnScore(word, afinn):
            total = 0
            if word in afinn:
                total += afinn[word]
            return total
        # end

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

        for tweet in tweets:
            for tag in tweet.split():
                if tag.startswith("#"):
                    hashtagCount+=1

            tweet = preprocessTweets.processTweet(tweet)
            if len(tweet)==0:
                continue
            #print(tweet)
            words = tweet.split(' ')
            total = 0
            for word in words:
                wordCount += 1
                if word not in stopWords:
                    #word = porter.stem(word)
                    #print (word)
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

        # get yahoo finance data
        yahoo = financeData()
        historical_data = yahoo.getYahooData(keyword, today)
        print(historical_data)

        positive_score = round(float(positive_score),2)
        negative_score = round(float(negative_score),2)
        neutral_score = round(float(neutral_score),2)
        open_price = round(float(historical_data['Open']),2)
        close_price = round(float(historical_data['Close']),2)
        high_price = round(float(historical_data['High']),2)
        low_price = round(float(historical_data['Low']),2)
        volume = int(historical_data['Volume'])
        total_words = wordCount
        total_hashtag = hashtagCount

        # print("positive_score:  " + str(positive_score))
        # print("negative_score:  " + str(negative_score))
        # print("neutral_score:  " + str(neutral_score))
        # print("open_price:  " + str(open_price))
        # print("close_price:  " + str(close_price))
        # print("high_price:  " + str(high_price))
        # print("low_price:  " + str(low_price))
        # print("volume:  " + str(volume))
        # print("total_words:  " + str(total_words))
        # print("total_hashtag:  " + str(total_hashtag))
        # print()

        # positive_score =  17.05
        # negative_score =  1.14
        # neutral_score = 81.82
        # open_price =  219.96
        # close_price =  219.97
        # high_price =  220.59
        # low_price = 219.13
        # volume =  12763561.0
        # total_words =  1144
        # total_hashtag =  42

        #feature_Lists = [['positive_score', 17.05],['negative_score',1.14],['neutral_score', 81.82],['open_price', 219.96],['close_price', 219.97],
         #                ['high_price', 220.59],['low_price',219.13],['volume',12763561.0],['total_words',1144],['total_hashtag',42]]

        feature_Lists = [['positive_score', positive_score], ['negative_score', negative_score], ['neutral_score', neutral_score],['open_price', open_price], ['close_price', close_price],['high_price', high_price], ['low_price', low_price], ['volume', volume], ['total_words', total_words],
                         ['total_hashtag', total_hashtag]]

        row_list = [positive_score, negative_score , neutral_score, open_price, close_price, high_price, low_price,
                                      volume, total_words,total_hashtag]

        #print(row_list)
        feature_df = pd.DataFrame([row_list], columns=['positive_score', 'negative_score','neutral_score', 'open_price','close_price','high_price', 'low_price','volume','total_words','total_hashtag'])

        #print(keyword + "***********")
        # create model object
        modelBuild = ModelBuild(keyword)

        pred_Lists = []
        # Classify the real-time test data
        pred_Lists.append(modelBuild.KNN_Model(feature_df))
        #print(pred_Lists)
        pred_Lists.append(modelBuild.NB_Model(feature_df))
        # print(pred_Lists)
        pred_Lists.append(modelBuild.Logist_Model(feature_df))
        # print(pred_Lists)
        newfeatures_df = feature_df
        newfeatures_df.drop(["high_price", "low_price", "volume", "total_words", "total_hashtag"], axis=1, inplace=True)
        # print(newfeatures_df)
        pred_Lists.append(modelBuild.SVM_Model(newfeatures_df))
        # print(pred_Lists)
        pred_Lists.append(modelBuild.DecisionTree_Model(newfeatures_df))
        #print(pred_Lists)
        pred_Lists.append(modelBuild.XGBoost_Model(newfeatures_df))
        # print()
        pred_Lists.append(modelBuild.Rand_Model(newfeatures_df))
        #print(pred_Lists)

        return pred_Lists, feature_Lists, positive_score, negative_score, neutral_score

