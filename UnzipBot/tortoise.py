import os
import shutil
import zipfile
from UnzipBot.functions import absolute_paths, progress
import rarfile
import mimetypes
import time
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from moviepy.editor import VideoFileClip

# Manually add .3gp file extension to video MIME types
mimetypes.add_type('video/3gpp', '.3gp')

# Telegram group topic ID where messages will be forwarded
GROUP_TOPIC_CHAT_ID = -1002107123962

# Telegram topic IDs
ERROR_TOPIC_ID = 18
FILES_TOPIC_ID = 20

tortoise_filter = filters.create(lambda _, __, query: query.data.lower() == "tortoise")

@Client.on_callback_query(tortoise_filter)
async def _tortoise(unzipbot, callback_query):
    start = datetime.now()
    msg = callback_query.message.reply_to_message
    await callback_query.message.delete()
    file_name = msg.document.file_name
    file_size = msg.document.file_size
    #if file_size > 1524288000:
      #  await msg.reply("Files with size more than 500 MB aren't allowed.", quote=True)
     #   return
    
    try:
        main = await msg.reply("Downloading...", quote=True)
        file = await msg.download(progress=progress, progress_args=(main, "Downloading..."))
        await main.edit("Extracting Files...")
        extract_dir = os.path.join("downloads", os.path.splitext(file_name)[0])
        os.makedirs(extract_dir, exist_ok=True)
        contents = []
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                contents = zip_ref.namelist()
                zip_ref.extractall(extract_dir)
        elif file_name.endswith(".rar"):
            with rarfile.RarFile(file, 'r') as rar_ref:
                contents = rar_ref.namelist()
                rar_ref.extractall(extract_dir)
        else:
            await msg.reply("Unsupported file format.", quote=True)
            return

        con_msg = await msg.reply("Checking Contents for you...", quote=True)
        constr = "\n".join(contents)
        ans = "**Contents** \n\n" + constr
        if len(ans) > 4096:
            await con_msg.edit("Checking Contents for you... \n\nSending as file...")
            with open("contents.txt", "w") as f:
                f.write(ans)
            await msg.reply_document("contents.txt")
            os.remove("contents.txt")
        else:
            await msg.reply(ans)
        await con_msg.delete()

        extracted_files = [i async for i in absolute_paths(extract_dir)]
        
        for file_path in extracted_files:
            mime_type, _ = mimetypes.guess_type(file_path)
            try:
                if mime_type and mime_type.startswith('video'):
                    # Use moviepy to get video duration and thumbnail
                    video = VideoFileClip(file_path)
                    duration = video.duration
                    thumbnail_path = f"{file_path}_thumbnail.jpg"
                    video.save_frame(thumbnail_path, t=duration / 2)  # Save thumbnail at half duration
                    video.close()
                    
                    # Send video with thumbnail
                    sent_message = await unzipbot.send_video(
                        callback_query.from_user.id,
                        file_path,
                        thumb=thumbnail_path,
                        duration=int(duration)
                    )
                    
                    # Forward the sent message to the group topic
                #    await unzipbot.forward_messages(GROUP_TOPIC_CHAT_ID, callback_query.from_user.id, sent_message.id)
                    
                    # Remove temporary thumbnail file
                    os.remove(thumbnail_path)
                elif mime_type and mime_type.startswith('image'):
                    sent_message = await unzipbot.send_photo(callback_query.from_user.id, file_path)
                else:
                    sent_message = await unzipbot.send_document(callback_query.from_user.id, file_path)
                
                # Forward the sent message to the group topic
                await unzipbot.forward_messages(GROUP_TOPIC_CHAT_ID, callback_query.from_user.id, sent_message.id)
          
            except FloodWait as e:
                print(f"FloodWait error: sleeping for {e.x} seconds")
                time.sleep(e.x)

        stop = datetime.now()
        await msg.reply(
            f"**Extraction Done Successfully..! \n\nTook {round((stop - start).total_seconds() / 60, 2)} minutes\n\nMade With ❤️ By @botio_devs**", parse_mode=enums.ParseMode.MARKDOWN)
    except rarfile.RarCannotExec:
        error_message = "**ERROR :** This File is possibly bugged. Cannot extract content. \n\n" \
                        "This may happen when a file's extension is manually changed to `.zip`/`.rar` even when file isn't in that format. \n\n" \
                        "Try with some other file please."
        await unzipbot.send_message(callback_query.from_user.id, error_message)
        await unzipbot.send_message(GROUP_TOPIC_CHAT_ID, error_message, reply_to_message_id=ERROR_TOPIC_ID)
         
    except Exception as e:
        error_message = f"**ERROR : **{str(e)}\n\n Send a message to botio_devs_discuss to resolve and report the issue."
        print(f"Unexpected error: {e}")  # Debug: Print unexpected errors
        await unzipbot.send_message(callback_query.from_user.id, error_message)
        await unzipbot.send_message(GROUP_TOPIC_CHAT_ID, error_message, reply_to_message_id=ERROR_TOPIC_ID)
        
    finally:
        if os.path.isdir("downloads"):
            shutil.rmtree("downloads")
