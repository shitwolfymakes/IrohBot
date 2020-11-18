"""Thanks to https://realpython.com/twitter-bot-python-tweepy/ for walking me through the basics of this"""

import tweepy


def main():
    # auth to twitter
    auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET_KEY")
    auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")

    # create api object
    api = tweepy.API(auth)

    # create tweet
    tweet_quote(api)


def tweet_quote(api):
    pass


if __name__ == '__main__':
    main()
