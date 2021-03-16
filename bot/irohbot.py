"""Thanks to https://realpython.com/twitter-bot-python-tweepy/ for walking me through the basics of this"""
import json
import logging
import os
import random
import time
from datetime import datetime, date

import requests
import schedule
import tweepy

from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()
    logger.info("Restarting!")
    api.update_status("Restarting at %s!" % datetime.now())
    schedule.every().day.at("16:00").do(tweet_quote, api) # do() is a wrapper for functools.partial(), so use commas

    while True:
        logger.info("Running jobs...")
        schedule.run_pending()
        follow_followers(api)
        time.sleep(30)


def tweet_quote(api):
    logger.info("Time to tweet!")
    if is_mako_day():
        logger.info("Celebrating Mako")
        tweet_mako(api)

    quote = pick_quote()
    status = quote[1]

    # if quote has linked media
    if quote[2] is not None:
        filename = 'temp.jpg'
        request = requests.get(str(quote[2]), stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            if quote[3] is not None:
                status = "%s Art source: %s" % (quote[1], quote[3])
            api.update_with_media(filename, status=status)
            os.remove(filename)
        else:
            print("Unable to download image")
    else:
        # just tweet the line
        api.update_status(status=status)
    logger.info("Tweet posted")


def is_mako_day():
    today = date.today().__str__()
    mako_day = "07-21"
    if today[5:] == mako_day:
        return True
    return False


def tweet_mako(api):
    api.update_with_media("mako_day.png", status="Thank you for everything <3")


def pick_quote():
    with open("iroh_wisdom.json") as json_file:
        data = json.load(json_file)
    data = data["wisdom"]
    quote = random.randrange(0, len(data))
    return tuple(data[quote].values())


def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()


if __name__ == '__main__':
    main()
