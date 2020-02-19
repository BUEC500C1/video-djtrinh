import tweepy
import configparser


class twitter_scrapper():

    def __init__(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        auth = tweepy.OAuthHandler(config.get('auth', 'consumer_key').strip(),
                                   config.get('auth', 'consumer_secret').strip())
        auth.set_access_token(config.get('auth', 'access_token').strip(),
                              config.get('auth', 'access_secret').strip())
        self.api = tweepy.API(auth)

    def get_user_pic(self, username):
        try:
            u = self.api.get_user(username)
            return u.profile_image_url_https
        except tweepy.error.TweepError:
            return ""

    def get_users_tweets(self, username):
        try:
            tweets = self.api.user_timeline(screen_name=username, count=20, include_rts=True, result_type="recent",
                                    include_entities=True,
                                    tweet_mode='extended',
                                    lang="en")
            return tweets
        except tweepy.error.TweepError:
            return ""

    def search_twitter(self, username, product):
        filt = '-filter:retweets'
        tweet_list = []

        if(product != ""):
            # Collect tweets based on product only
            i = 0
            for tweet in tweepy.Cursor(self.api.search,
                                       q=product,
                                       count=100,
                                       result_type="recent",
                                       include_entities=True,
                                       tweet_mode='extended',
                                       lang="en").items():
                i = i + 1

                tweet_proc = "".join(tweet.full_text.lower().split())
                if(tweet_proc.find(
                        "".join(product.lower().split())) != -1):
                    if(self.spam_checker(tweet_proc) == False):
                        tweet_list.append(tweet.full_text)

                if i == 1500:
                    break

        # Collect tweets from username
        if(username != ""):
            search_words = "@"+username+filt

            i = 0
            for tweet in tweepy.Cursor(self.api.search,
                                       q=search_words,
                                       count=100,
                                       result_type="recent",
                                       include_entities=True,
                                       tweet_mode='extended',
                                       lang="en").items():

                i = i + 1
                tweet_proc = "".join(tweet.full_text.lower().split())
                if(tweet_proc.find(
                        "".join(product.lower().split())) != -1):
                    if(self.spam_checker(tweet_proc) == False):
                        tweet_list.append(tweet.full_text)

                if i == 1500:
                    break

        return tweet_list

    def spam_checker(self, string):
        spam_keywords = ["sweepstakes", "contest", "ebay", "sale", "http/1.1",
                         "giveaway", "case", "bestbuy", "walmart", "unlocked",
                         "factory", "buynow", "call:", "call", "deals"]
        for word in spam_keywords:
            if(string.find(word) != -1):
                return True

        return False

    def grab_pictures(self, username):
        img_list = []
        for tweet in tweepy.Cursor(self.api.search,
                                   q=username,
                                   count=100,
                                   result_type="recent",
                                   include_entities=True,
                                   tweet_mode='extended',
                                   lang="en").items():
            if 'media' in tweet.entities:
                for medium in tweet.entities['media']:
                    if medium['type'] == 'photo':
                        img_list.append(medium['media_url'])

        return img_list
