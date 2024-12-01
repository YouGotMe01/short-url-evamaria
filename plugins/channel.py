import asyncio
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import BadRequest
from info import CHANNELS, UPDATES_CHNL
from database.ia_filterdb import save_file
from utils import add_chnl_message, get_poster, temp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        mv_naam, year, languages = await add_chnl_message(text)
        if mv_naam is not None:
            languages_str = " ".join(languages) if languages else None
            mv_naam = mv_naam.replace(".", " ")
            if year.isdigit():
                caption = f"<b>#PreDvDUpdate:\n<blockquote>🧿 <u>𝐍𝐚𝐦𝐞</u> : <code>{mv_naam}</code>\n📆 <u>𝐘𝐞𝐚𝐫</u> : {year}\n"
            if languages_str:
                caption += f"🎙️<u>𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞</u> : {languages_str}</blockquote>"
            else:
                caption += f"</blockquote>\n"
            caption += "Copy only Movie Name & Paste In👇\n---»<a href=https://t.me/movie_request_group_links> ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜɪɴɢ ɢʀᴏᴜᴘ ʟɪɴᴋs </a>«---</b>"
            await bot.send_message(
                chat_id=UPDATES_CHNL,
                text=caption,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            logger.info(f'{mv_naam} {year} - Update Sent to Channel!')
            await asyncio.sleep(5)
            return
