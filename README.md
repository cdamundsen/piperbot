# piperbot
Bluesky bot that posts a around 300 characters of H. Beam Piper's novella Four Day Planet every hour

Currently I'm running it via a cron job on my desktop machine like this:
0 30 * * * export BSKY_NAME="<bsky username>"; export BSKY_PASS="<bsky password>"; export BSKY_DM_TARGET="<bsky username of account to alert when various things occur>"; export BSKY_BOOK_NAME="<path to the text file of the book"; source <path to python virtualenv>/bin/activate; <path to the source dirctory>/piperbot/piperbot.py
