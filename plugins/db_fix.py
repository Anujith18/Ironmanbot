# -*- coding: utf-8 -*-
from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery
import logging

CHANNELS = [-1002015288592]

# സ്റ്റാൻഡേർഡ് ഫിൽട്ടർ ബോട്ട് രീതിയിലുള്ള ഫയൽ ഫെച്ചിങ് ഹാൻഡിലർ
@Client.on_callback_query(filters.regex(r"^file#"))
async def get_file_from_database(client: Client, query: CallbackQuery):
    try:
        # ബട്ടൺ ഡാറ്റയിൽ നിന്ന് ഫയൽ ഐഡി വേർതിരിക്കുന്നു
        _, file_id = query.data.split("#", 1)
        
        await query.answer("ഫയൽ എടുത്തുകൊണ്ടിരിക്കുന്നു...", show_alert=False)
        
        # ചാനലിൽ നിന്നോ ഡാറ്റാബേസിൽ നിന്നോ ഫയൽ യൂസറിലേക്ക് അയക്കുന്നു
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption="<b>🎬 ഫയൽ വിജയകരമായി നൽകിയിരിക്കുന്നു!</b>",
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        logging.error(f"Error sending file from database channel: {e}")
        await query.answer(
            "❌ ക്ഷമിക്കണം, ഈ ഫയൽ ലഭ്യമല്ല അല്ലെങ്കിൽ ലിങ്ക് എക്സ്പയർ ആയിരിക്കുന്നു!",
            show_alert=True
        )
