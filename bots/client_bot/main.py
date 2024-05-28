import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)
from telegram.ext import filters
import os
import handlers
from dotenv import load_dotenv

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start_app():
    load_dotenv()

    application = (
        ApplicationBuilder().token(os.environ.get("TELEGRAM_BOT_TOKEN")).build()
    )

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CallbackQueryHandler(handlers.categories, pattern="^C-.+"))
    application.add_handler(
        CallbackQueryHandler(handlers.save_product, pattern="^S-.+")
    )
    application.add_handler(MessageHandler(filters.TEXT, handlers.text))

    application.run_polling()


if __name__ == "__main__":
    start_app()

# add a recommendation system

# Semantic search functionality
#### [DONE] display a search button on the homepage
#### [DONE] when clicked it will accept a text
#### send the query to a vector database
#### retrieve the search by relevance/time

# A filter functionality
#### [DONE] display a filter button on the homepage
#### when clicked ...

# Browse by category
#### [DONE] display a categories button on the homepage
#### [DONE]when clicked it will display sub categories button
#### if no categories then show product paginations

# Pagination

# Display product details
#### query and display complete details of a product

# [DONE] Store user information
#### [DONE] on first /start command store user data

# Store click data
#### update the database when handler is executed

# [DONE] Send user to private chat of seller
#### [DONE] add the link of the user on the callback query of the user

# Send user who want to sell to the appropriate bot chat.
#### add a button on the home page that says sell

# Give more info
#### add a button on home page that says other
#### when clicked it will display other buttons

# Notifications
#### add a button on the home page that says notifications
#### ...

# Saved
#### add a button on the homp page that says Saved
#### display a list of saved items
