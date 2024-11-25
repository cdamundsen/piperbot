# piperbot
Bluesky bot that posts a around 300 characters of a text file every hour. Currently working my way through H. Beam Piper's public domain writings.

Currently I'm running it via a cron job on my desktop machine like this:

59 * * * * export BSKY_NAME="\<bsky username\>;"; export BSKY_PASS="\<bsky password\>"; export BSKY_DM_TARGET="\<bsky username of account to alert when various things occur\>"; export BSKY_BOOK_NAME="\<path to the text file of the book\>"; source \<path to python virtualenv\>/bin/activate; cd \<path to where the session file is stored\> && \<path to the source dirctory\>/piperbot/piperbot.py
