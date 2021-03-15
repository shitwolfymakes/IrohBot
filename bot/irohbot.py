"""Thanks to https://realpython.com/twitter-bot-python-tweepy/ for walking me through the basics of this"""
import datetime
import json
import logging
import os
import random
import time

import requests
import schedule

from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()
    api.update_status("Restarting!")
    schedule.every().day.at("16:00").do(tweet_quote, api) # do() is a wrapper for functools.partial(), so use commas

    while True:
        n = schedule.idle_seconds()
        logger.info("Checking time...")
        logger.info("Time to next job: %d seconds" % n)
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        schedule.run_pending()


def tweet_quote(api):
    logger.info("Time to tweet!")
    if is_mako_day():
        logger.info("Celebrating Mako")
        tweet_mako(api)

    quote = pick_quote()

    if quote[2] is not None:
        filename = 'temp.jpg'
        request = requests.get(str(quote[2]), stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

            api.update_with_media(filename, status=quote[1])
            os.remove(filename)
        else:
            print("Unable to download image")
    else:
        api.update_status(status="Hello World!")
    logger.info("Tweet posted")


def is_mako_day():
    today = datetime.date.today().__str__()
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


if __name__ == '__main__':
    main()
