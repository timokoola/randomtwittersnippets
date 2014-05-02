from twython import Twython
import sys
import os
from collections import Counter
import re
import argparse  # requires 2.7
import time
import json
import codecs
import pprint
from image_generator import ImageGenerator
import textwrap
import time


class TweepyHelper:

    def __init__(self, keyfile):
        f = open(keyfile)
        lines = f.readlines()
        f.close()
        consumerkey = lines[0].split("#")[0]
        consumersecret = lines[1].split("#")[0]
        accesstoken = lines[2].split("#")[0]
        accesssec = lines[3].split("#")[0]

        self.api = Twython(consumerkey, consumersecret, accesstoken, accesssec)


def handle_command_line():
    parser = argparse.ArgumentParser(
        description="Tweets a text format book, line by line.")
    parser.add_argument(
        "-i", "--id", help="Run a test run, get nth tweet",
        default="8")
    parser.add_argument("-f", "--fontfile",
                        help="fontfile location")
    parser.add_argument("-k", "--keyfile",
                        help="Twitter account consumer and accesstokens")
    parser.add_argument("-b", "--bookfile", help="Book to be read")
    parser.add_argument("-l", "--logfile",
                        help="File contains ino about Line we are on.", default="tweetedids.txt")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = handle_command_line()

    book = codecs.open(args.bookfile, "r", "utf-8")
    tweets = json.load(book)
    book.close()

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tweets[args.id])

    api = (TweepyHelper(args.keyfile)).api
    ig = ImageGenerator(tweets[args.id], args)
    ig.generate()
    ig.save()

    fn = open(ig.file_name, "rb")

    lines = textwrap.wrap(tweets[args.id]["text"], 100)
    s = api.update_status_with_media(status=lines[0], media=fn)

    for l in lines[1:]:
        s = api.update_status(status=l, in_reply_to_status_id=s["id"])
