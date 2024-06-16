import os
import shutil
import time
import zipfile
import rarfile
from datetime import datetime
from pyrogram import Client, filters
from UnzipBot.functions import absolute_paths, progress
from pyrogram.errors import FloodWait

GROUP_ID = 2107123962
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
    if file_size > 1524288000:
        await msg.reply("Files with size more than 500 MB aren't allowed.", quote=True)
        return
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
        
        number = 0
        file_ids = []
        for file in extracted_files:
            try:
                number += 1
                sending = await msg.reply(f"**Uploading... ({number}/{len(extracted_files)})**")
                sent_message = await msg.reply_document(file, quote=False, progress=progress,
                                         progress_args=(sending, f"Uploading... ({number}/{len(extracted_files)})"), disable_notification=True)
                file_ids.append(sent_message.document.file_id)
                await sending.delete()
            except FloodWait as e:
                print(f"FloodWait error: sleeping for {e.x} seconds")
                time.sleep(e.x)

        for file_id in file_ids:
            await unzipbot.send_document(GROUP_ID, file_id, message_thread_id=FILES_TOPIC_ID)

        stop = datetime.now()
        await msg.reply(
            f"Extraction Done Successfully..! \n\nTook {round((stop - start).total_seconds() / 60, 2)} minutes \n\nFor more bots visit @MysteryBots")
    except rarfile.RarCannotExec:
        await msg.reply("**ERROR :** This File is possibly bugged. Cannot extract content. \n\n"
                        "This may happen when a file's extension is manually changed to `.zip`/`.rar` even when file isn't in that format. \n\n"
                        "Try with some other file please.", quote=True)
    except Exception as e:
        error_message = f"**ERROR : **{str(e)}\n\nForward this message to @MysteryBots to solve this problem."
        print(f"Unexpected error: {e}")  # Debug: Print unexpected errors
        await unzipbot.send_message(GROUP_ID, error_message, message_thread_id=ERROR_TOPIC_ID)
    finally:
        if os.path.isdir("downloads"):
            shutil.rmtree("downloads")
