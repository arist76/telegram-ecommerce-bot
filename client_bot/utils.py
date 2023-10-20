import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
from typing import Any

ITEMS_PER_PAGE = 5

DIR = os.path.dirname(os.path.abspath(__file__))


def escape_characters(input_string):
    # telegram characters to escape for MD text
    characters_to_escape = [
        "_",
        # "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]
    escaped_string = ""
    for char in input_string:
        if char in characters_to_escape:
            escaped_string += "\\" + char
        else:
            escaped_string += char
    return escaped_string


def reset_text_context(handler_func):
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        context.user_data.clear()
        await handler_func(update, context, *args, **kwargs)

    return wrapper


