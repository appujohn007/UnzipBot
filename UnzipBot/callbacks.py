from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Data import Data


home_filter = filters.create(lambda _, __, query: query.data.lower() == "home")
about_filter = filters.create(lambda _, __, query: query.data.lower() == "about")
help_filter = filters.create(lambda _, __, query: query.data.lower() == "help")

# Callbacks
@Client.on_callback_query(home_filter)
async def _home(unzipbot, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.id
    user = await unzipbot.get_me()
    mention = user.mention
    await unzipbot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=Data.START.format(callback_query.from_user.mention, mention),
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )

@Client.on_callback_query(about_filter)
async def _about(unzipbot, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.id
    await unzipbot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=Data.ABOUT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.home_button),
    )



@Client.on_callback_query(help_filter)
async def _help(unzipbot, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.id
    await unzipbot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_button),
    )




