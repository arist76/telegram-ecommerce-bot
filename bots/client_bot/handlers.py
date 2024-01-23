from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import ContextTypes, ConversationHandler
import utils
import buttons
import models

@utils.reset_text_context
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles "/start" command, checks if a user exists and handles registration"""
    # check if the user exists
    updater_user = update.effective_user

    if await models.User.exists():
        await context.bot.send_message(
            update.effective_chat.id,
            text="Choose from the below keyboard buttons",
            reply_markup=buttons.home(),
        )
    else:
        user = models.User(
            id = updater_user.id,
            is_bot = updater_user.is_bot,
            first_name = updater_user.first_name,
            last_name = updater_user.last_name,
            username = updater_user.username,
        )
        user.create()

        await context.bot.send_message(
            update.effective_chat.id, text="Welcome, this is how to use the bot..."
        )


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles any incoming text including keyboard buttons"""

    # Handle different text_mode as per "context.user_data.text_mode"
    match context.user_data.get("text_mode"):
        case "search":  # search mode
            await context.bot.send_message(
                update.effective_chat.id,
                text="Hooray, You have successfully made a search",
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
                    pass

                case "Saved 💾":
                    pass

                case "Other ...":
                    pass

                case _:  # for any arbitrary text not specified above
                    await context.bot.send_message(
                        update.effective_chat.id, text="This input is not recognized"
                    )


@utils.reset_text_context
async def categories(update: Update, context: ContextTypes):
    query = update.callback_query
    category_id = int(query.data[2:])
    inline = buttons.categories(category_id)

    if inline == None:
        products = models.Product.paginate_by_category(category_id, 1)

        for product in products:
            await product(update, context, product)

        if len(products) == utils.ITEMS_PER_PAGE:
            await context.bot.send_message(
                update.effective_chat.id,
                text="👀.",
                reply_markup=buttons.see_more(1),
            )
    else:
        await query.edit_message_reply_markup(reply_markup=inline)



###################### Unregistered Views ######################

@utils.reset_text_context
async def product(
    update: Update, context: ContextTypes.DEFAULT_TYPE, product: models.Product
):
    title = f"*Title*: {product.name}\n"
    price = f"*Price*: {product.price}"

    text = utils.escape_characters(title + price)

    await context.bot.send_message(
        update.effective_chat.id,
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=buttons.product(),
    )

@utils.reset_text_context
async def see_more(update: Update, context: ContextTypes.DEFAULT_TYPE, page_no):
    await context.bot.send_message(
        update.effective_chat.id,
        text = "...",
        reply_markup= buttons.see_more(page_no)
    )