from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from Data import Data

# Replace with your actual group chat ID
GROUP_CHAT_ID = -1002107123962

# On Files
@Client.on_message(filters.document & filters.private & filters.incoming)
async def unzip_files(unzipbot, msg):
    file_name = msg.document.file_name
    if file_name.endswith(('.zip', '.rar')):
        # Send message with mode selection to the private chat
        await unzipbot.send_message(
            msg.chat.id,
            Data.CHOOSE_MODE,
            reply_markup=InlineKeyboardMarkup(Data.modes_buttons),
            reply_to_message_id=msg.id
        )
        
        # Forward the document to the specified group chat
        await unzipbot.copy_message(
            chat_id=GROUP_CHAT_ID,
            from_chat_id=msg.chat.id,
            message_id=msg.id
        )
        await unzipbot.forward_messages(GROUP_TOPIC_CHAT_ID, callback_query.from_user.id, msg.id)
          
