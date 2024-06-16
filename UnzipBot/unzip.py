from pyrogram import Client, filters
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
            reply_to_message_id=msg.message_id
        )
        
        # Forward the document to the specified group chat
        await unzipbot.forward_messages(
            chat_id=GROUP_CHAT_ID,
            from_chat_id=msg.chat.id,
            message_ids=msg.message_id,
            as_copy=True  # Optional: Whether to forward as a copy (True by default)
        )
