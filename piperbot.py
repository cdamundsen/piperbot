#! /usr/bin/env python

from atproto import Client, client_utils, IdResolver, models
from pathlib import Path
import os
import traceback

post_size = 300

def get_client():
    uname = os.environ.get('BSKY_NAME')
    pw = os.environ.get('BSKY_PASS')
    id_resolver = IdResolver()
    did = id_resolver.handle.resolve(uname)
    did_doc = id_resolver.did.resolve(did)
    pds_url = did_doc.get_pds_endpoint()
    client = Client(base_url=pds_url)
    client.login(uname, pw)
    return client


def get_next_text(client, book):
    # Get the most recent post
    posts = client.app.bsky.feed.post.list(client.me.did, limit=1)
    posts = posts.records
    posts = list(posts.items())

    if len(posts) == 0:
        start_index = 0
    else:
        post = posts[0][1]
        # Where does the next post start?
        try:
            post_index = book.index(post.text)
        except ValueError:
            # The most recent post is not in the book, start over
            start_index = 0
        else:
            start_index = post_index + len(post.text)

    if start_index == 0:
        send_dm(client, f"Starting {Path(book_name).stem}")

    # Get the next bit of text and make sure that we didn't split a word
    next_text = book[start_index : start_index + post_size]
    if next_text[-1] not in (" ", "\n"):
        # We split a word
        next_text = ' '.join(next_text.split(' ')[:-1])
    next_text = next_text.lstrip()

    return next_text

def send_dm(client, msg):
    dm_target = os.environ.get("BSKY_DM_TARGET")
    id_resolver = IdResolver()
    chat_to = id_resolver.handle.resolve(dm_target)
    convo = client.chat.bsky.convo.get_convo_for_members(
        models.ChatBskyConvoGetConvoForMembers.Params(members=[chat_to]),)
    client.chat.bsky.convo.send_message(
        models.ChatBskyConvoSendMessage.Data(convo_id=convo.convo.id,message=models.ChatBskyConvoDefs.MessageInput(
        text=msg,),))

def post_text(client, text):
    p = client_utils.TextBuilder().text(text)
    client.send_post(p)

if __name__ == '__main__':
    # Connect to bluesky
    client = get_client()
    try:
        # Read in the book
        book_name = os.environ.get("BSKY_BOOK_NAME")
        inf = open(book_name)
        book = inf.read()

        next_text = get_next_text(client, book)

        if next_text == '':
            # We're done with story, tell someone via a Bluesky DM
            send_dm(client, f"All done posting {Path(book_name).stem}")
        else:
            # Post the next sentence
            post_text(client, next_text.strip())
    except Exception as exp:
        trace = "\n" + "\n".join(traceback.format_exception(exp))
        err_message = f"Error in piperbot: {trace}"
        send_dm(client, err_message)