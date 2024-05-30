#! /usr/bin/env python

from atproto import Client, client_utils, IdResolver, models
from pathlib import Path
import os

book_name = '/Users/amundsen/src/piperbot/Four-Day Planet.txt'
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
    post = list(posts.records.items())[0][1]

    # Where does the next post start?
    post_index = book.index(post.text)
    start_index = post_index + len(post.text)

    # Get the next bit of text and make sure that we didn't split a word
    next_text = book[start_index : start_index + post_size]
    if next_text[-1] not in (" ", "\n"):
        # We split a word
        next_text = ' '.join(next_text.split(' ')[:-1])
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

    # Read in the book
    inf = open(book_name)
    book = inf.read()

    next_text = get_next_text(client, book)

    if next_text == '':
        # We're done with story, tell someone via a Bluesky DM
        send_dm(client, f"All done posting {Path(book_name).stem}")
    else:
        # Post the next sentence
        post_text(client, next_text.strip())