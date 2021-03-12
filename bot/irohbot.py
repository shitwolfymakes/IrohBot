"""Thanks to https://realpython.com/twitter-bot-python-tweepy/ for walking me through the basics of this"""
import datetime
import logging
import os
import time

import requests
import schedule

from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()
    tweet_quote(api)
    return
    schedule.every().day.at("16:00").do(tweet_quote, api) # do() is a wrapper for functools.partial(), so use commas

    while True:
        schedule.run_pending()
        time.sleep(1)


def tweet_quote(api):
    print("test!")
    if is_mako_day():
        tweet_mako()
    #TODO: Get a quote from the json
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


def is_mako_day():
    today = datetime.date.today().__str__()
    mako_day = "07-21"
    if today[5:] == mako_day:
        return True
    return False


def tweet_mako():
    pass


def pick_quote():
    return [None, "Hello with a picture!", "https://hannahjanewrites.com/wp-content/uploads/2015/02/iroh2.png", None]


if __name__ == '__main__':
    main()
