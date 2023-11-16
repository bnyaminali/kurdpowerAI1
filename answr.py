#!/usr/bin/env python

import os
import sys
from Bard import Chatbot

try:
    BARD_TOKEN = os.environ['AIzaSyC81I0PK1VNGUJivVVeWJEvZVVo5e33VPA']
    if 'de' in sys.argv:
        print(f'AIzaSyC81I0PK1VNGUJivVVeWJEvZVVo5e33VPA: {BARD_TOKEN}')
except Exception as e:
    print(f"ERROR: Cannot get token from environment:{e}")
    sys.exit(1)

chatbot = Chatbot(BARD_TOKEN)


def get_answer(message: str) -> str:
    """
    Get a response from a chatbot for a given message.

    Args:
        message (str): The message to send to the chatbot.

    Returns:
        str: The response from the chatbot.
    """
    response = chatbot.ask(message)
    return response["content"]


if __name__ == "__main__":
    msg = input("Enter your message: ")
    ana = get_answer(msg)
    print(ana)
