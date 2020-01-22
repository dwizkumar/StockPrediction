import tweepy
import re


class TwitterData:

    """
    authenticate function makes a connection with Twitter and returns a connection handle
    ------------
    input:
        consumer_key, consumer_secret, access_token_key, access_token_secret
    ------------
    output:
        connection handle
    ------------
    citation:
        https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04

    """

    def authenticate(self):

        consumer_key =  'jlXoDyJtfEoK8KtjBrgWGghQs'
        consumer_secret = 'cDCBSyGCdJYls5q4HGIvXfe71kTJ1FG69d3CD1A5mspv7N4o59'
        access_token_key = '1152416889861263360-kbrnBqg6IS4X1i5od25NaiTJydCB3V'
        access_token_secret = '6jQOyHCgrViC5PBYohHv8QhLQlbnmKTjRIiE2K7Aq77kW'

        maxTweets = 200

        # OAuth process, using the keys and tokens
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)

        # Creation of the actual interface, using authentication
        api = tweepy.API(auth)

        return api
     #end


    """
      getTweets function uses the API handler and fetches the real-time tweets based on
      the keyword or ticker
      -----------
      input:
        api handler
        start date - current date
      ----------- 
      output:
        real-time tweets
      -----------
     https://www.programcreek.com/python/example/76301/tweepy.Cursor     
    """
    def getTweets(self, api, keyword, date_since):
        tweets = tweepy.Cursor(api.search,
                               q=keyword ,
                               lang="en",
                               since=date_since).items(200)
        #
        # # Iterate on tweets
        listTweet = []
        ads = ['pic.twitter.com','@RobinhoodApp','ACTIVE TRADERS']
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        bad_chars = [';', ':', '!', "*",'…']
        uniqueTweets = []

        for tweet in tweets:
            flag = True
            result = re.sub(r'http\S+', '', tweet.text)
            # result = re.sub('…','', result)
            # result.encode('ascii','ignore').decode('ascii')
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
                    listTweet.append(result)
        return listTweet
    #end

