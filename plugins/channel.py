from pyrogram import Client, filters
from info import CHANNELS, UPDATES_CHNL
from database.ia_filterdb import save_file
from utils import add_chnl_message

media_filter = filters.document | filters.video


@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    for file_type in ("document", "video"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    media.file_type = file_type
    media.caption = message.caption
    text = await save_file(media)
    if text is not None:
        final = await add_chnl_message(text)
        if final is not None:
            cap = "#PreDvDUpdate:\n\n"
            await bot.send_message(chat_id=UPDATES_CHNL, text=f"<b>{cap}<code>{final}</code>\n\nCopy & Paste In Group To Search\n---»<a href=https://t.me/isaimini_updates/110> ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜɪɴɢ ɢʀᴏᴜᴘ ʟɪɴᴋs </a>«---</b>", disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
