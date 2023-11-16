#!/usr/bin/env python
"""
main file
"""
import tbot
from typing import Any
import os
import logging
import json
import sys
from flask import redirect, url_for
from flask import Flask, request, Response  # render_template
from telegram import Bot, Update  # ChatAction

sys.dont_write_bytecode = True
try:
    TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
except Exception as e:
    print("ERROR: Cannot get token from environment:%s" % e)
    sys.exit(1)

app = Flask(__name__)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)


@app.route('/', methods=['GET'])
def tet() -> str:
    """Redirect to https://t.me/Googl_Bard_bot."""
    #return redirect(url_for('https://t.me/Googl_Bard_bot'))
    return "<meta http-equiv='refresh' content='0; url=https://t.me/Googl_Bard_bot'>"


@app.route('/', methods=['POST'])
def index() -> Any:
    """Handle incoming webhook messages."""
    # ---
    msg = request.get_json()
    # ---
    print(f'method: {request.method} ')
    print("message-->" + str(msg))
    # ---
    update = Update.de_json(msg, bot)
    # ---
    rbot = tbot.MyBot(update, bot, logger)
    # ---
    rbot.main()
    # ---
    return Response("ok", status=200)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
