#! /usr/bin/env python

from atproto import Client, client_utils
import os
import sys

book_name = '/Users/amundsen/src/piperbot/FourDayPlanet.txt'

if __name__ == '__main__':
    # Connect to bluesky
    client = Client()
    uname = os.environ.get('bsky_name')
    pw = os.environ.get('bsky_pass')
    client.login(uname, pw)

    # Read in the book
    inf = open(book_name)
    book = inf.read().splitlines()

    # Get the most recent post
    posts = client.app.bsky.feed.post.list(client.me.did, limit=1)
    post = list(posts.records.items())[0][1]
    sentence = post.text

    # Are we done?
    if sentence == book[-1]:
        sys.exit(0)

    # Figure out where we are in the book and get the next sentence
    sentence_index = book.index(sentence)
    next_sentence = book[sentence_index + 1]

    # Post the next sentence
    p = client_utils.TextBuilder().text(next_sentence)
    client.send_post(p)