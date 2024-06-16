from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Data:
    # Start Message
    START = "Hey. \n\nWelcome to Unzip Bot \n\nI can unzip & unrar files you send me and upload them to our private chat. \nI will also total the contents & number of files."

    # About Message
    ABOUT = """
    **     A̲B̲O̲U̲T̲__M̲E̲**

    **ɪᴀᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ғᴏʀ ᴜɴᴢɪᴘᴘɪɴɢ ғɪʟᴇs**

    **ⒹⓃⒶ : [ＰＹＲＯＧＲＡＭ](docs.pyrogram.org)**
    **ⒼⒺⓃⒺ : [ＰＹＴＨＯＮ](www.python.org) \n\nDeveloper : [Mყʂƚҽɾყ Bσყ](https://t.me/MysteryxD)**
    **ⒻⒶⓉⒽⒺⓇ : [ＡＰＰＵＳ](https://t.me/Appuz_007)**
    **ⒻⒶⓂⒾⓁⓎ: [.ｉｏ ｄｅｖｓ](https://t.me/botio_devs)**
    """

    # Help Message
    HELP = """
**ɴᴇᴇᴅ ʜᴇʟᴘ ?? 🙃 **

🄼🅈 🄹🄾🄱
ɪᴀᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴜɴᴢɪᴘ ʏᴏᴜʀ .ᴢɪᴘ.ғɪʟᴇs

🄷🄾🅆 🅃🄾 🅄🅂🄴 🄼🄴 !!

sᴇɴᴅ ᴍᴇ ᴀɴʏ .ᴢɪᴘ ғɪʟᴇs ᴀɴᴅ sɪᴛ ʙᴀᴄᴋ

**Available Commands** :-

/start - Check if bot is alive.
/help - This Message.
/about - About this bot

**Support** - @botio_devs_discuss
"""

    # Choose Mode Message
    CHOOSE_MODE = "**CHOOSE MODE ** \n\nChoose a mode from below to start extracting files..."

    # Home Button
    home_button = [[InlineKeyboardButton(text="🏠 Return Home 🏠", callback_data="home")]]

    # Modes Buttons
    modes_buttons = [
        [InlineKeyboardButton("Extract", callback_data="tortoise")],
        [InlineKeyboardButton("How to Use me ⁉️", callback_data="help")]
    ]

    # Main Buttons
    buttons = [
        [
            InlineKeyboardButton("How to Use me ⁉️", callback_data="help"),
            InlineKeyboardButton("📤 About 📤", callback_data="about")
        ],
        [InlineKeyboardButton("♥ More Amazing bots ♥", url="https://t.me/botio_devs")],
        [InlineKeyboardButton("🎨 Support Group 🎨", url="https://t.me/botio_devs_discuss")]
    ]
