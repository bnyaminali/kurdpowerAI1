#!/usr/bin/env python
"""

"""
import answr
from datetime import datetime, timezone
from typing import Any
from flask import Response
import json
import sys

sys.dont_write_bytecode = True


class MyBot:
    """
    This class is the main bot class.
    """

    def __init__(self, update, bot, logger):
        """
        Initialize the class.
        """
        self.update = update
        self.bot = bot
        self.logger = logger
        self.welcome = (
            'Welcome! Send me a message starting with "ask" to get an answer.'
        )
        self.chatid = ""
        self.msgid = ""
        self.msg_text = ""

    def main(self) -> Any:
        """
        Execute the main functionality of the program.
        """
        ia = self.handle_message()
        if not ia:
            return

        mm = self.read_message()
        if not mm:
            return

        self.get_answer()

        return

    def get_answer(self) -> None:
        """
        Retrieves an answer based on the message text and sends it as a message.
        """
        answer = answr.get_answer(self.msg_text)
        self.bot_send_message(answer)

    def read_message(self) -> bool:
        """
        Reads and processes the user's message.
        """
        if not self.update.message.text:
            return False
        self.msg_text = self.update.message.text
        if self.msg_text.startswith("/start"):
            self.bot_send_message(self.welcome)
            return False
        if not self.msg_text.lower().startswith("ask"):
            self.bot_send_message(self.welcome)
            return False
        self.msg_text = self.msg_text[3:]
        if self.msg_text.strip() == "":
            return False

        return True

    def get_message_age(self) -> float:
        """
        Get the age of the message in milliseconds, based on the message date or edit date.
        """
        event_time = self.update.message.date
        if self.update.message.edit_date:
            event_time = self.update.message.edit_date

        event_age = (datetime.now(timezone.utc) - event_time).total_seconds()
        event_age_ms = event_age * 1000
        self.logger.info(str(event_age_ms))
        return event_age_ms

    def timeout(self, max_duration: int = 60000) -> bool:
        """
        Check if the current message has timed out, i.e. if its age in milliseconds
        exceeds a given duration.
        """
        try:
            event_age_ms = self.get_message_age()
        except Exception as e:
            self.logger.info(f"timeout except: {e}")
            return True

        if event_age_ms < max_duration:
            return False
        else:
            return True

    def handle_message(self) -> bool:
        """
        This function handles incoming chat messages.
        """

        if not self.update.message and self.update.effective_chat:
            self.bot.send_message(
                chat_id=self.update.effective_chat.id, text="send text"
            )
            return False

        self.chatid = self.update.message.chat_id
        self.msgid = self.update.message.message_id
        message = self.update.message

        if self.timeout():
            self.bot_send_message(
                "Timeout! Please use /start to restart the bot.")
            return False

        chat_ = getattr(message, "chat", None)
        if not chat_:
            self.bot_send_message("Join @Googl_Bard_bot")
            return False
        else:
            chat_username = getattr(chat_, "username", None)
            if not chat_username or chat_username not in [
                "Googl_Bard_bot",
                "Ibrahim_Qasim",
            ]:
                self.bot_send_message("Join @Googl_Bard_bot")
                return False
        return True

    def bot_send_message(self, text):
        """
        Sends a message using the Telegram bot API.
        """
        try:
            self.bot.send_message(
                chat_id=self.chatid, text=text, reply_to_message_id=self.msgid
            )
        except Exception as e:
            print("bot_send_message Error : %s" % str(e))
