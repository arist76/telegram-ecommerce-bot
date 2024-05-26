from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import models


def home():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Categories 🗂"), KeyboardButton("Sell 💸")],
            [KeyboardButton("Search 🔍"), KeyboardButton("Filter 🎯")],
            [KeyboardButton("Notifications 🔔"), KeyboardButton("Saved 💾")],
            [KeyboardButton("Other ...")],
        ]
    )


async def categories(parent_id: int = 0, cols: int = 2):
    pattern = "C"
    categories = models.Category.all({"parent" : parent_id})

    if not categories:
        return None

    markup = [
        InlineKeyboardButton(
            "🔙",
            callback_data=f"{pattern}-{models.Category.grand_parent(parent_id)}",
        )
    ]
    for category in categories:
        markup.append(
            InlineKeyboardButton(
                f"{category.name} {category.emoji}",
                callback_data=f"{pattern}-{category.id}",
            )
        )

    # slice into columns
    inline = InlineKeyboardMarkup(
        [markup[i : i + cols] for i in range(0, len(markup), cols)]
    )

    return inline


def seller() -> InlineKeyboardMarkup:
    seller_bot_url = "https://t.me/suradummybot"

    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("got to seller", url=seller_bot_url)]]
    )


def product():
    pattern = "P"  # callback route pattern
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Buy 💸", callback_data=f"{pattern}-buy")],
            [
                InlineKeyboardButton("Get  🔔", callback_data=f"{pattern}-notify"),
                InlineKeyboardButton("Save 💾", callback_data=f"{pattern}-save"),
            ],
        ]
    )


def see_more(page_no: int, data: [] = []):
    pattern = "L"  # callback route pattern
    data = "|".join(data)
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "See more ...",
                    callback_data=f"{pattern}-{page_no+1}-{data}",
                )
            ]
        ]
    )
