import uuid
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    InputMediaPhoto,
)
from telegram.ext import ContextTypes, ConversationHandler
import utils
import buttons
import models
import httpx


@utils.reset_text_context
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles "/start" command, checks if a user exists and handles registration"""
    # check if the user exists
    updater_user = update.effective_user
    if models.User.exists(updater_user.id):
        # if False:
        await context.bot.send_message(
            update.effective_chat.id,
            text="Choose from the below keyboard buttons",
            reply_markup=buttons.Home(),
        )
    else:
        user = models.User(
            data={
                "id": updater_user.id,
                "is_bot": updater_user.is_bot,
                "first_name": updater_user.first_name,
                "last_name": updater_user.last_name,
                "username": updater_user.username,
            }
        )

    await context.bot.send_message(
        update.effective_chat.id, text="Welcome, this is how to use the bot..."
    )


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles any incoming text including keyboard buttons"""

    # Handle different text_mode as per "context.user_data.text_mode"
    match context.user_data.get("text_mode"):
        case "search":  # search mode
            products, _, _, _ = models.Product.all(q=update.effective_message.text)
            for p in products:
                await product(update, context, p)

            await context.bot.send_message(
                update.effective_chat.id,
                text="Hooray, You have successfully made a search",
                reply_markup=buttons.Home(),
            )
            context.user_data["text_mode"] = None

        case _:  # default text mode, which is the home keyboard button
            match update.message.text:
                case "Categories 🗂":
                    await context.bot.send_message(
                        update.effective_chat.id,
                        text="Top level categories",
                        reply_markup=await buttons.categories(),
                    )
                case "Sell 💸":
                    await context.bot.send_message(
                        update.effective_chat.id,
                        text="Go to sell bot",
                        reply_markup=buttons.seller(),
                    )

                case "Search 🔍":
                    await context.bot.send_message(
                        update.effective_chat.id,
                        text="What do you want to search for",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                    context.user_data["text_mode"] = "search"

                case "Filter 🎯":
                    pass

                case "Notifications 🔔":
                    await context.bot.send_message(
                        update.effective_chat.id,
                        text="What up",
                    )

                case "Saved 💾":
                    user_id = update.effective_user.id
                    saved_products = models.Product.user_saved_products(user_id)
                    for p in saved_products:
                        await product(update, context, p)

                    total_saved_products = len(saved_products)
                    await context.bot.send_message(
                        update.effective_chat.id,
                        text=f"You have saved {total_saved_products} in total",
                    )

                case "Other ...":
                    pass

                case _:  # for any arbitrary text not specified above
                    await context.bot.send_message(
                        update.effective_chat.id, text="This input is not recognized"
                    )


@utils.reset_text_context
async def categories(update: Update, context: ContextTypes):
    query = update.callback_query

    try:
        category_id = uuid.UUID(query.data[2:])
    except ValueError:  # default to base categories for invalid uuid
        category_id = None
    inline = await buttons.categories(category_id)

    if inline == None:
        products, count, prev, next = models.Product.all(category=category_id)

        for p in products:
            await product(update, context, p)

        if (count - (utils.ITEMS_PER_PAGE * (next - 1))) > 0:
            await context.bot.send_message(
                update.effective_chat.id,
                text="👀.",
                reply_markup=buttons.see_more(next),
            )
        else:
            text = "End of products" if count > 0 else "No products in the catalogue"
            await context.bot.send_message(update.effective_chat.id, text=text)
    else:
        await query.edit_message_reply_markup(reply_markup=inline)


###################### Unregistered Views ######################


@utils.reset_text_context
async def product(
    update: Update, context: ContextTypes.DEFAULT_TYPE, product: models.Product
):
    title = f"*Title*: {product.name}\n"
    price = f"*Price*: {product.price}"
    image_temp = [
        "https://dlcdnwebimgs.asus.com/gain/f69cfad3-af20-403e-ad93-1ffb91604d82/w800",
        "https://dlcdnwebimgs.asus.com/gain/3eb89add-c844-4c13-aa49-f4441f5dbbef/w800",
        "https://dlcdnwebimgs.asus.com/gain/3eb89add-c844-4c13-aa49-f4441f5dbbef/w800",
    ]

    images = [InputMediaPhoto(image) for image in image_temp]

    text = utils.escape_characters(title + price)
    if images:
        await context.bot.send_media_group(
            update.effective_chat.id,
            media=images,
            caption=text,
            parse_mode="MarkdownV2",
        )
        await context.bot.send_message(
            update.effective_chat.id,
            text="Actions.",
            reply_markup=buttons.product(product),
        )


@utils.reset_text_context
async def see_more(update: Update, context: ContextTypes.DEFAULT_TYPE, page_no):
    await context.bot.send_message(
        update.effective_chat.id, text="...", reply_markup=buttons.see_more(page_no)
    )


@utils.reset_text_context
@utils.set_user_uuid
async def save_product(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    product_uuid = query.data[1:]
    print(product_uuid, context.user_data.get("user_uuid"))
    data = {"product": product_uuid, "user": context.user_data.get("user_uuid")}
    res = httpx.post(f"{models.model_backend}saved/", data=data)

    if res.status_code == 201:
        await query.edit_message_reply_markup(
            reply_markup=buttons.product_saved(product_uuid),
        )
