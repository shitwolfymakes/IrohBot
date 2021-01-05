"""Thanks to https://realpython.com/twitter-bot-python-tweepy/ for walking me through the basics of this"""
import datetime
import logging
import time

import schedule

from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()
    schedule.every(10).seconds.do(tweet_quote, api)     # do() is a wrapper for functools.partial(), so use commas

    while True:
        schedule.run_pending()
        time.sleep(1)


def tweet_quote(api):
    print("test!")
    if is_mako_day():
        tweet_mako()
    #TODO: Get a quote from the json
    #TODO: Craft tweet with tuple containing quote data
    #TODO: Post tweet


def is_mako_day():
    today = datetime.date.today().__str__()
    mako_day = "07-21"
    if today[5:] == mako_day:
        return True
    return False


def tweet_mako():
    pass


if __name__ == '__main__':
    main()
