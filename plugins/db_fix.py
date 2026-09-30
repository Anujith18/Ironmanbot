# -*- coding: utf-8 -*-
from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery
import logging

# കോൺഫിഗറേഷൻ അല്ലെങ്കിൽ ചാനൽ ഐഡി സെറ്റിംഗ്സ്
CHANNELS = [-1002015288592]

# ഡാറ്റാബേസ് ലിങ്ക് വഴി ഫയൽ ഫെച്ച് ചെയ്ത് യൂസറിന് അയക്കുന്ന കോഡ്
@Client.on_callback_query(filters.regex(r"^get_db_file#"))
async def get_db_file_handler(client: Client, query: CallbackQuery):
    try:
        # Callback data-ൽ നിന്ന് ഫയൽ ഐഡി അല്ലെങ്കിൽ കീവേഡ് എടുക്കുന്നു
        _, file_key = query.data.split("#", 1)
        
        await query.answer("ഫയൽ ഡാറ്റാബേസിൽ നിന്ന് എടുത്തുകൊണ്ടിരിക്കുന്നു...", show_alert=False)
        
        # നിങ്ങളുടെ ഡാറ്റാബേസ് മോഡ്യൂളിൽ നിന്ന് ഫയൽ തിരയുന്ന ലോജിക് ഇവിടെ നൽകാം
        # ഉദാഹരണത്തിന്: file_data = await db.get_file_by_id(file_key)
        
        # ഡാറ്റാബേസ് ചാനലിൽ നിന്നോ ക്യാഷിൽ നിന്നോ ഫയൽ യൂസറുടെ ഇൻബോക്സിലേക്ക് അയക്കുന്നു
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_key,
            caption="<b>📂 ഡാറ്റാബേസിൽ നിന്ന് വിജയകരമായി ഫയൽ നൽകിയിരിക്കുന്നു!</b>",
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        logging.error(f"DB File fetch error: {e}")
        await query.answer(
            "❌ ക്ഷമിക്കണം, ഈ ഡാറ്റാബേസ് ഫയൽ ലിങ്ക് ലഭ്യമല്ല അല്ലെങ്കിൽ എറർ വന്നിരിക്കുന്നു!",
            show_alert=True
        )
