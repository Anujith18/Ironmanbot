import logging
import os
import re
from urllib.parse import quote
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters

logger = logging.getLogger(__name__)

# --- SERIALS MAPPING & GET FILE LINKS ---
SERIALS_MAPPING = {
    "kanmashi": "Kanmashi",
    "karnan": "Karnan",
    "valyettan": "Valyettan",
    "pranayavilasam": "Pranayavilasam",
    "durga": "Durga",
    "chembarathy": "Chembarathy",
    "saregamapa": "SaReGaMaPa",
    "saregamapa_lil_champs": "SaReGaMaPa Lil Champs",
    "kudumbasametham": "Kudumbasametham",
    "meghasandhesham": "Meghasandhesham",
    "seethayanam": "Seethayanam",
    "krishnagadha": "Krishnagadha",
    "meghasandesam": "Meghasandesam",
    "aval_arundhati": "Aval Arundhati",
    "akale": "Akale",
    "snehapoorvam_shyama": "Snehapoorvam Shyama",
    "mangalyam": "Mangalyam",
    "manathe_kottaram": "Manathe Kottaram",
    "ashwathi_nakshatram": "Ashwathi Nakshatram",
    "kudumbashree_sharada": "Kudumbashree Sharada",
    "bigg_boss": "Bigg Boss",
    "taste_time": "Taste Time",
    "sindhu_bhairavi": "Sindhu Bhairavi",
    "comedy_cooks": "Comedy Cooks",
    "ivar_vivahitharayal": "Ivar Vivahitharayal",
    "oru_kochu_swapnam": "Oru Kochu Swapnam",
    "advocate_anjali": "Advocate Anjali",
    "kattathe_kilikoodu": "Kattathe Kilikoodu",
    "ee_puzhayum_kadannu": "Ee Puzhayum Kadannu",
    "sindoorapottu": "Sindoorapottu",
    "star_singer": "Star Singer",
    "teacheramma": "Teacheramma",
    "mazha_thorum_munpe": "Mazha Thorum Munpe",
    "pavithram": "Pavithram",
    "ishtam_mathram": "Ishtam Mathram",
    "santhwanam": "Santhwanam",
    "snehakkoottu": "Snehakkoottu",
    "mounaragam": "Mounaragam",
    "patharamattu": "Patharamattu",
    "amma_manassu": "Amma Manassu",
    "chempaneer_poovu": "Chempaneer Poovu",
    "dharmma_yoddhavu_garudan": "Dharmma Yoddhavu Garudan",
    "othiri_othiri_swapnangal": "Othiri Othiri Swapnangal",
    "ottashikharam": "Ottashikharam",
    "archana_chechi_llb": "Archana Chechi LLB",
    "super_kanmani": "Super Kanmani",
    "marimayam": "Marimayam",
    "oru_chiri_iru_chiri_bumper_chiri": "Oru Chiri Iru Chiri Bumper Chiri",
    "the_great_family_challenge": "The Great Family Challenge",
    "roopavathi": "Roopavathi",
    "thenmavin_kombath": "Thenmavin Kombath",
    "punnaram": "Punnaram",
    "anju_sundarikal": "Anju Sundarikal",
    "amme_mookambike": "Amme Mookambike",
    "peythozhiyathe": "Peythozhiyathe",
    "chattambipparu": "Chattambipparu",
    "hridayam": "Hridayam",
    "kanyadaanam": "Kanyadaanam",
    "swayamavarapanthal": "Swayamavarapanthal",
    "mangalyam_thanthunanena": "Mangalyam Thanthunanena"
}

GET_FILE_LINKS = [
    "https://telegram.me/Anujith1bot?start=getfile-Kanmashi",
    "https://telegram.me/Anujith1bot?start=getfile-Karnan",
    "https://telegram.me/Anujith1bot?start=getfile-Valyettan",
    "https://telegram.me/Anujith1bot?start=getfile-Pranayavilasam",
    "https://telegram.me/Anujith1bot?start=getfile-Durga",
    "https://telegram.me/Anujith1bot?start=getfile-Chembarathy",
    "https://telegram.me/Anujith1bot?start=getfile-SaReGaMaPa",
    "https://telegram.me/Anujith1bot?start=getfile-SaReGaMaPa-Lil-Champs",
    "https://telegram.me/Anujith1bot?start=getfile-Kudumbasametham",
    "https://telegram.me/Anujith1bot?start=getfile-Meghasandhesham",
    "https://telegram.me/Anujith1bot?start=getfile-Seethayanam",
    "https://telegram.me/Anujith1bot?start=getfile-Krishnagadha",
    "https://telegram.me/Anujith1bot?start=getfile-Meghasandesam",
    "https://telegram.me/Anujith1bot?start=getfile-Aval-Arundhati",
    "https://telegram.me/Anujith1bot?start=getfile-Akale",
    "https://telegram.me/Anujith1bot?start=getfile-Snehapoorvam-Shyama",
    "https://telegram.me/Anujith1bot?start=getfile-Mangalyam",
    "https://telegram.me/Anujith1bot?start=getfile-Manathe-Kottaram",
    "https://telegram.me/Anujith1bot?start=getfile-Ashwathi-Nakshatram",
    "https://telegram.me/Anujith1bot?start=getfile-Kudumbashree-Sharada",
    "https://telegram.me/Anujith1bot?start=getfile-Bigg-Boss",
    "https://telegram.me/Anujith1bot?start=getfile-Taste-Time",
    "https://telegram.me/Anujith1bot?start=getfile-Sindhu-Bhairavi",
    "https://telegram.me/Anujith1bot?start=getfile-Comedy-Cooks",
    "https://telegram.me/Anujith1bot?start=getfile-Ivar-Vivahitharayal",
    "https://telegram.me/Anujith1bot?start=getfile-Oru-Kochu-Swapnam",
    "https://telegram.me/Anujith1bot?start=getfile-Advocate-Anjali",
    "https://telegram.me/Anujith1bot?start=getfile-Kattathe-Kilikoodu",
    "https://telegram.me/Anujith1bot?start=getfile-Ee-Puzhayum-Kadannu",
    "https://telegram.me/Anujith1bot?start=getfile-Sindoorapottu",
    "https://telegram.me/Anujith1bot?start=getfile-Star-Singer",
    "https://telegram.me/Anujith1bot?start=getfile-Teacheramma",
    "https://telegram.me/Anujith1bot?start=getfile-Mazha-Thorum-Munpe",
    "https://telegram.me/Anujith1bot?start=getfile-Pavithram",
    "https://telegram.me/Anujith1bot?start=getfile-Ishtam-Mathram",
    "https://telegram.me/Anujith1bot?start=getfile-Santhwanam",
    "https://telegram.me/Anujith1bot?start=getfile-Snehakkoottu",
    "https://telegram.me/Anujith1bot?start=getfile-Mounaragam",
    "https://telegram.me/Anujith1bot?start=getfile-Patharamattu",
    "https://telegram.me/Anujith1bot?start=getfile-Amma-Manassu",
    "https://telegram.me/Anujith1bot?start=getfile-Chempaneer-Poovu",
    "https://telegram.me/Anujith1bot?start=getfile-Dharmma-Yoddhavu-Garudan",
    "https://telegram.me/Anujith1bot?start=getfile-Othiri-Othiri-Swapnangal",
    "https://telegram.me/Anujith1bot?start=getfile-Ottashikharam",
    "https://telegram.me/Anujith1bot?start=getfile-Archana-Chechi-LLB",
    "https://telegram.me/Anujith1bot?start=getfile-Super-Kanmani",
    "https://telegram.me/Anujith1bot?start=getfile-Marimayam",
    "https://telegram.me/Anujith1bot?start=getfile-Oru-Chiri-Iru-Chiri-Bumper-Chiri",
    "https://telegram.me/Anujith1bot?start=getfile-The-Great-Family-Challenge",
    "https://telegram.me/Anujith1bot/roopavathi",
    "https://telegram.me/Anujith1bot?start=getfile-Thenmavin-Kombath",
    "https://telegram.me/Anujith1bot?start=getfile-Punnaram",
    "https://telegram.me/Anujith1bot?start=getfile-Anju-Sundarikal",
    "https://telegram.me/Anujith1bot?start=getfile-Amme-Mookambike",
    "https://telegram.me/Anujith1bot?start=getfile-Peythozhiyathe",
    "https://telegram.me/Anujith1bot?start=getfile-Chattambipparu",
    "https://telegram.me/Anujith1bot?start=getfile-Hridayam",
    "https://telegram.me/Anujith1bot?start=getfile-Kanyadaanam",
    "https://telegram.me/Anujith1bot?start=getfile-Swayamavarapanthal",
    "https://telegram.me/Anujith1bot?start=getfile-Mangalyam-Thanthunanena"
]

async def plugin_auto_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post or update.message
    if not message:
        return

    file_name = ""
    if message.document:
        file_name = message.document.file_name
    elif message.video:
        file_name = message.video.file_name or message.caption or "Unknown Video"
    elif message.caption:
        file_name = message.caption

    if not file_name:
        return

    file_name_lower = file_name.lower()
    detected_serial = None
    matched_key = None
    
    for key, serial_name in SERIALS_MAPPING.items():
        formatted_key = key.replace("_", " ")
        if formatted_key in file_name_lower or key in file_name_lower:
            detected_serial = serial_name
            matched_key = key
            break
            
    if not detected_serial:
        detected_serial = os.path.splitext(file_name)[0]

    season_match = re.search(r'S(\d+)', file_name, re.IGNORECASE)
    season = season_match.group(1) if season_match else "01"
    
    episode_match = re.findall(r'E(\d+(?:-\d+)?)', file_name, re.IGNORECASE)
    if not episode_match:
        episode_match = re.findall(r'(\d+)', file_name)
    episode = episode_match[0] if episode_match else "1"

    qualities = re.findall(r'(\d{3,4}p)', file_name, re.IGNORECASE)
    quality = qualities[0] if qualities else "720p"

    caption_text = (
        f"<b>🍁 Anujith Allu TV Serials 🍁</b>\n\n"
        f"📁 <b>File Name :</b> {detected_serial}\n"
        f"🎞 <b>Season :</b> {season}\n"
        f"📌 <b>Episode :</b> {episode}\n"
        f"🎬 <b>Quality :</b> {quality}"
    )

    get_file_url = None
    if matched_key:
        clean_matched_key = matched_key.replace("_", "").replace("-", "").lower()
        for link in GET_FILE_LINKS:
            clean_link = link.replace("-", "").replace("_", "").lower()
            if clean_matched_key in clean_link:
                get_file_url = link
                break
    
    if not get_file_url:
        get_file_url = f"https://telegram.me/Anujith1bot?start=getfile-{detected_serial.replace(' ', '-')}"

    keyboard = [[InlineKeyboardButton("📥 Get File", url=get_file_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # നിങ്ങളുടെ ബോട്ടിന്റെ ഡാറ്റാബേസ് ചാനൽ ക്രമീകരണങ്ങൾ അനുസരിച്ച് ഇവിടെ ചാറ്റ് ഐഡി നൽകാം
        # നിലവിലുള്ള ചാനൽ പോസ്റ്റിലേക്ക് ഫോട്ടോയോടൊപ്പം ഫോർമാറ്റ് ചെയ്ത് അയക്കാൻ:
        banner_image = "YOUR_BANNER_IMAGE_URL_HERE" # ഇവിടെ നിങ്ങളുടെ ബാനർ ലിങ്ക് നൽകാം
        
        await message.reply_photo(
            photo=banner_image,
            caption=caption_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Plugin post error: {e}")
