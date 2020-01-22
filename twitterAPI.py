import GetOldTweets3 as got
import re

"""
 GetOldTweets3 downloads tweets between the specified date and returns tweets
 based on organization's ticker.
 
 Removes emojis, ads, and non-ascii characters before saving into a file
 
 -------------
 input: 
    start date
    end date
    query search
    max tweets per day
    
 output:
    daily tweets in specific file
  -------------    
  
  Citations:
  https://developers.google.com/chart/interactive/docs/basic_load_libs
  
"""

for j in range(7, 31):
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch('FB')\
                                                   .setSince("2019-04-" + str(j)) \
                                                   .setUntil("2019-04-" + str(j+1)) \
                                                   .setMaxTweets(100) \
                                                   .setLang('en')


        create_text = []
        ads = ['pic.twitter.com','@RobinhoodApp','ACTIVE TRADERS']

        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)

        bad_chars = [';', ':', '!', "*",'…']
        uniqueTweets = []

        # print(tweetCriteria.lang)
        for i in range(1, tweetCriteria.maxTweets):
            flag = True
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)[i]
            result = re.sub(r'http\S+', '', tweet.text)
            # result = re.sub('…','', result)
            #result.encode('ascii','ignore').decode('ascii')
            result = "".join(filter(lambda i: i not in bad_chars, result))
            result = emoji_pattern.sub(r'', result)
            result = re.sub(r'[^\x00-\x7F]+', ' ', result)
            for ad in ads:
                if ad in result:
                    flag = False
                    break
            if flag:
                if result not in uniqueTweets:
                    uniqueTweets.append(result)
                    create_text.append(result + "||")
                    print(result + "||")
                # print(str(i)+ " ----> " + tweet.date.strftime("%Y-%m-%d"))

        # current_dt = datetime.datetime.now()
        path = './data/FB/' + tweet.date.strftime("%Y-%m-%d") + '.txt'
        print(path)
        with open(path, "w") as file:
           file.write(' '.join(create_text))