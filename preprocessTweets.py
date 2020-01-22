import re

"""
 processTweets cleans the tweets by correcting the spelling or split word
 -------------
 input:
    tweet
 -------------
 output:
    cleaned tweet 
"""
# start process_tweet
def processTweet(tweet):
    #print(tweet)
    tweet = tweet.lower()
    tweet = re.sub("n't"," not", tweet)
    tweet = re.sub("'s"," is", tweet)
    tweet = re.sub("avg", "average", tweet)
    tweet = re.sub("dis", "this", tweet)
    tweet = re.sub("tnx", "thanks", tweet)
    tweet = re.sub("opt", "option", tweet)
    tweet = re.sub("mkt", "market", tweet)
    tweet = re.sub("st", "street", tweet)
    tweet = re.sub("nyse", "nice", tweet)
    tweet = re.sub("amzn", "amazon", tweet)
    tweet = re.sub("ya", "yes", tweet)
    tweet = re.sub("didn", "did not", tweet)
    tweet = re.sub("don", "do not", tweet)
    tweet = re.sub("performanceperwatt", "performance per watt", tweet)
    tweet = re.sub("vp", "vice president", tweet)
    tweet = re.sub("min", "minimum", tweet)
    tweet = re.sub("app", "application", tweet)
    tweet = re.sub("subs", "substitute", tweet)
    tweet = re.sub("interestreeted", "interested", tweet)
    tweet = re.sub("mostreet", "street", tweet)
    tweet = re.sub("doesn", "does not", tweet)
    tweet = re.sub("info", "information", tweet)
    tweet = re.sub("trudeau", "trade", tweet)
    tweet = re.sub("yearlydelivered", "yearly delivered", tweet)
    tweet = re.sub("profitpacked", "profit packed", tweet)
    tweet = re.sub("dailyfree", "daily free", tweet)
    tweet = re.sub("optionions", "opinion", tweet)
    tweet = re.sub("optionion", "opinion", tweet)
    tweet = re.sub("tech", "technology", tweet)
    tweet = re.sub("bio", "biography", tweet)
    tweet = re.sub("ppl", "people", tweet)
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    tweet = re.sub('@[^\s]+', ' ', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub('-','', tweet)
    tweet = re.sub('_','',tweet)
    tweet = re.sub('\.','', tweet)
    tweet = re.sub(r'\$.+','', tweet)
    tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet)
    tweet = re.sub("([a-zA-z]+[0-9]+)|([0-9]+)"," ", tweet)
    tweet = tweet.strip('\'"')
    tweet = tweet.strip()
    #print(tweet)
    return tweet
# end

"""
getStopWordList function makes a list of stopwords based on stopword file and 
returns the stopword's list
----------
input:
    None
----------
output:
    stopword's list    
"""
# start get stop word
def getStopWordList():
  stopWords = []

  stopWords.append('AT_USER')
  stopWords.append('URL')

  fp = open('./data/stopwords.txt', 'r')
  line = fp.readline()
  while line:
      word = line.strip()
      stopWords.append(word)
      line = fp.readline()
  fp.close()
  return stopWords
# end