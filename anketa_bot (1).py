import logging
from telegram import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, ContextTypes, ConversationHandler,
    MessageHandler, filters, CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Bot token and channel IDs
TOKEN = "8588890290:AAGsNtrhVf1I0bwhSO-X9ur8TCmeMlZ1K2g"
BRIDE_CHANNEL_ID = -1002541786621
GROOM_CHANNEL_ID = -1002885285470

# States for ConversationHandler
(
    SELECTING_ROLE, NAME, AGE, HEIGHT, WEIGHT,
    NATIONALITY, NATIONALITY_MANUAL,
    LOCATION, LOCATION_MANUAL,
    # Bride-specific states
    BRIDE_JOB, BRIDE_MARITAL, BRIDE_CHILDREN, BRIDE_VILOYAT,
    BRIDE_VILOYAT_MANUAL, BRIDE_KUYOV_AJRASHGAN, BRIDE_KUYOV_AJRASHGAN_MANUAL,
    BRIDE_IKKINCHI_ROZGOR, BRIDE_IKKINCHI_ROZGOR_MANUAL,
    BRIDE_KUYOV_YOSH, BRIDE_KUYOV_TALAB, BRIDE_USERNAME,
    # Groom-specific states
    GROOM_MARITAL, GROOM_JOB, GROOM_KELIN_AJRASHGAN, GROOM_KELIN_AJRASHGAN_MANUAL,
    GROOM_HAQIDA, GROOM_KELIN_TALAB, GROOM_USERNAME,
    # Common
    CONTACT
) = range(29)


# ==================== YORDAMCHI FUNKSIYALAR ====================

def back_button_reply():
    """Oldingi savolga qaytish reply tugmasi"""
    return ReplyKeyboardMarkup(
        [[KeyboardButton("⬅️ Oldingi savolga qaytish")]],
        resize_keyboard=True, one_time_keyboard=True
    )


# ==================== SAVOLLARNI YUBORISH FUNKSIYALARI ====================

async def send_selecting_role(target, edit=False):
    keyboard = [
        [InlineKeyboardButton("👰‍♂️Kelin nomzod", callback_data="bride"),
         InlineKeyboardButton("🤵‍♂️ Kuyov nomzod", callback_data="groom")],
    ]
    text = "Assalomu alaykum! Anketa to'ldirib beruvchi botga hush kelibsiz 😊\n\nKelin nomzodmisiz yoki kuyov nomzodmisiz tanlang 👇"
    if edit and hasattr(target, 'edit_message_text'):
        await target.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await target.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def send_name_question(target, edit=False):
    if edit:
        await target.edit_message_text("Ismingiz nima?")
    else:
        await target.reply_text("Ismingiz nima?", reply_markup=ReplyKeyboardRemove())


async def send_age_question(target):
    await target.reply_text("Yoshingizni yozing?", reply_markup=back_button_reply())


async def send_height_question(target):
    await target.reply_text("Bo'yingiz necha santimetr?", reply_markup=back_button_reply())


async def send_weight_question(target):
    await target.reply_text("Vazningiz necha kilogramm?", reply_markup=back_button_reply())


async def send_nationality_question(target, edit=False):
    keyboard = [
        [InlineKeyboardButton("Oʻzbek🇺🇿", callback_data="nat_Oʻzbek🇺🇿"),
         InlineKeyboardButton("Qozoq🇰🇿", callback_data="nat_Qozoq🇰🇿")],
        [InlineKeyboardButton("Qirgʻiz🇰🇬", callback_data="nat_Qirgʻiz🇰🇬"),
         InlineKeyboardButton("Tojik🇹🇯", callback_data="nat_Tojik🇹🇯")],
        [InlineKeyboardButton("Metis", callback_data="nat_Metis"),
         InlineKeyboardButton("Tatar", callback_data="nat_Tatar")],
        [InlineKeyboardButton("Rus🇷🇺", callback_data="nat_Rus🇷🇺")],
        [InlineKeyboardButton("✍️ Qo'lda yozish", callback_data="nat_manual")],
        [InlineKeyboardButton("⬅️ Oldingi savolga qaytish", callback_data="nat_back")],
    ]
    if edit:
        await target.edit_message_text("Millatingiz?", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await target.reply_text("Millatingiz?", reply_markup=InlineKeyboardMarkup(keyboard))


async def send_location_question(target, edit=False):
    keyboard = [
        [InlineKeyboardButton("Toshkent sh.", callback_data="loc_Toshkent sh."),
         InlineKeyboardButton("Toshkent vil.", callback_data="loc_Toshkent vil.")],
        [InlineKeyboardButton("Samarqand", callback_data="loc_Samarqand"),
         InlineKeyboardButton("Buxoro", callback_data="loc_Buxoro")],
        [InlineKeyboardButton("Xorazm", callback_data="loc_Xorazm"),
         InlineKeyboardButton("Navoiy", callback_data="loc_Navoiy")],
        [InlineKeyboardButton("Qashqadaryo", callback_data="loc_Qashqadaryo"),
         InlineKeyboardButton("Surxondaryo", callback_data="loc_Surxondaryo")],
        [InlineKeyboardButton("Farg'ona", callback_data="loc_Farg'ona"),
         InlineKeyboardButton("Andijon", callback_data="loc_Andijon")],
        [InlineKeyboardButton("Namangan", callback_data="loc_Namangan"),
         InlineKeyboardButton("Jizzax", callback_data="loc_Jizzax")],
        [InlineKeyboardButton("Sirdaryo", callback_data="loc_Sirdaryo"),
         InlineKeyboardButton("QR", callback_data="loc_QR")],
        [InlineKeyboardButton("✍️ Qo'lda yozish", callback_data="loc_manual")],
        [InlineKeyboardButton("⬅️ Oldingi savolga qaytish", callback_data="loc_back")],
    ]
    if edit:
        await target.edit_message_text("Yashash joyingiz?", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await target.reply_text("Yashash joyingiz?", reply_markup=InlineKeyboardMarkup(keyboard))


def bride_marital_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Turmushga chiqmagan", callback_data="bm_Turmushga chiqmagan")],
        [InlineKeyboardButton("Ajrashgan", callback_data="bm_Ajrashgan")],
        [InlineKeyboardButton("Beva", callback_data="bm_Beva")],
        [InlineKeyboardButton("⬅️ Oldingi savolga qaytish", callback_data="bm_back")],
    ])


def bride_children_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Yo'q", callback_data="bc_Yo'q"),
         InlineKeyboardButton("1 ta", callback_data="bc_1 ta"),
         InlineKeyboardButton("2 ta", callback_data="bc_2 ta")],
        [InlineKeyboardButton("3 ta", callback_data="bc_3 ta"),
         InlineKeyboardButton("4 ta", callback_data="bc_4 ta"),
         InlineKeyboardButton("5 ta", callback_data="bc_5 ta")],
        [InlineKeyboardButton("⬅️ Oldingi savolga qaytish", callback_data="bc_back")],
    ])


def yes_no_manual_back_keyboard(prefix):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Ha", callback_data=f"{prefix}_Ha")],
        [InlineKeyboardButton("Yo'q", callback_data=f"{prefix}_Yo'q")],
        [InlineKeyboardButton("✍️ Qo'lda yozish", callback_data=f"{prefix}_manual")],
        [InlineKeyboardButton("⬅️ Oldingi savolga qaytish", callback_data=f"{prefix}_back")],
    ])


def groom_marital_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Uylanmagan", callback_data="gm_Uylanmagan")],
        [InlineKeyboardButton("Ajrashgan", callback_data="gm_Ajrashgan")],
        [InlineKeyboardButton("Oilali (ikkinchi ro'zg'orga)", callback_data="gm_Oilali (ikkinchi ro'zg'orga)")],
        [InlineKeyboardButton("⬅️ Oldingi savolga qaytish", callback_data="gm_back")],
    ])


# ==================== START ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await send_selecting_role(update.message)
    return SELECTING_ROLE


async def select_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    role = query.data
    context.user_data.clear()
    context.user_data["role"] = role
    await send_name_question(query, edit=True)
    return NAME


# ==================== INLINE TUGMA BOSILGANDA MATN YOZILSA ====================
# Bu funksiya inline tugma kutilayotgan state'larda foydalanuvchi matn yozsa javob beradi

async def wrong_input_for_inline(update: Update, context: ContextTypes.DEFAULT_TYPE, question_text):
    """Foydalanuvchi inline tugma kutilayotgan joyda matn yozsa"""
    await update.message.reply_text(
        f"❌ Iltimos, yuqoridagi tugmalardan birini bosing.\n\n{question_text}"
    )


# ==================== UMUMIY SAVOLLAR ====================

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await send_selecting_role(update.message)
        return SELECTING_ROLE
    context.user_data["name"] = update.message.text
    await send_age_question(update.message)
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await send_name_question(update.message)
        return NAME
    context.user_data["age"] = update.message.text
    await send_height_question(update.message)
    return HEIGHT


async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await send_age_question(update.message)
        return AGE
    context.user_data["height"] = update.message.text
    await send_weight_question(update.message)
    return WEIGHT


async def get_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await send_height_question(update.message)
        return HEIGHT
    context.user_data["weight"] = update.message.text
    await send_nationality_question(update.message)
    return NATIONALITY


# --- Millat (inline) ---
async def get_nationality(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "nat_back":
        await query.edit_message_text("Vazningiz necha kilogramm?")
        return WEIGHT
    if data == "nat_manual":
        await query.edit_message_text("Millatingiz?")
        await query.message.reply_text("Javobni yozing ✍️", reply_markup=back_button_reply())
        return NATIONALITY_MANUAL
    # Millatni olish (nat_ prefixini olib tashlash)
    context.user_data["nationality"] = data[4:]
    await send_location_question(query, edit=True)
    return LOCATION


async def get_nationality_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Millat savolida foydalanuvchi matn yozsa"""
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing yoki \"Qo'lda yozish\" tugmasini bosing.")
    return NATIONALITY


async def get_nationality_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await send_nationality_question(update.message)
        return NATIONALITY
    context.user_data["nationality"] = update.message.text
    await send_location_question(update.message)
    return LOCATION


# --- Yashash joyi (inline) ---
async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "loc_back":
        await send_nationality_question(query, edit=True)
        return NATIONALITY
    if data == "loc_manual":
        await query.edit_message_text("Yashash joyingiz?")
        await query.message.reply_text("Javobni yozing ✍️", reply_markup=back_button_reply())
        return LOCATION_MANUAL
    context.user_data["location"] = data[4:]
    role = context.user_data["role"]

    if role == "bride":
        await query.edit_message_text("Ish joyingiz haqida yozing?")
        return BRIDE_JOB
    else:
        await query.edit_message_text("Turmushdagi holatingiz?", reply_markup=groom_marital_keyboard())
        return GROOM_MARITAL


async def get_location_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yashash joyi savolida foydalanuvchi matn yozsa"""
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing yoki \"Qo'lda yozish\" tugmasini bosing.")
    return LOCATION


async def get_location_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await send_location_question(update.message)
        return LOCATION
    context.user_data["location"] = update.message.text
    role = context.user_data["role"]

    if role == "bride":
        await update.message.reply_text("Ish joyingiz haqida yozing?", reply_markup=back_button_reply())
        return BRIDE_JOB
    else:
        await update.message.reply_text("Turmushdagi holatingiz?", reply_markup=groom_marital_keyboard())
        return GROOM_MARITAL


# ==================== BRIDE FLOW ====================

async def bride_get_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await send_location_question(update.message)
        return LOCATION
    context.user_data["job"] = update.message.text
    await update.message.reply_text("Turmushdagi holatingiz?", reply_markup=bride_marital_keyboard())
    return BRIDE_MARITAL


async def bride_get_marital(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "bm_back":
        await query.edit_message_text("Ish joyingiz haqida yozing?")
        return BRIDE_JOB
    context.user_data["marital_status"] = data[3:]
    await query.edit_message_text("Ajrashgan bo'lsa farzandingiz?", reply_markup=bride_children_keyboard())
    return BRIDE_CHILDREN


async def bride_get_marital_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing.")
    return BRIDE_MARITAL


async def bride_get_children(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "bc_back":
        await query.edit_message_text("Turmushdagi holatingiz?", reply_markup=bride_marital_keyboard())
        return BRIDE_MARITAL
    context.user_data["children"] = data[3:]
    await query.edit_message_text("Boshqa viloyatga ketishga rozimisiz?", reply_markup=yes_no_manual_back_keyboard("bv"))
    return BRIDE_VILOYAT


async def bride_get_children_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing.")
    return BRIDE_CHILDREN


async def bride_get_viloyat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "bv_back":
        await query.edit_message_text("Ajrashgan bo'lsa farzandingiz?", reply_markup=bride_children_keyboard())
        return BRIDE_CHILDREN
    if data == "bv_manual":
        await query.edit_message_text("Boshqa viloyatga ketishga rozimisiz?")
        await query.message.reply_text("Javobni yozing ✍️", reply_markup=back_button_reply())
        return BRIDE_VILOYAT_MANUAL
    context.user_data["viloyat_rozi"] = data[3:]
    await query.edit_message_text("Kuyov ajrashgan bo'lsa rozimisiz?", reply_markup=yes_no_manual_back_keyboard("bka"))
    return BRIDE_KUYOV_AJRASHGAN


async def bride_get_viloyat_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing yoki \"Qo'lda yozish\" tugmasini bosing.")
    return BRIDE_VILOYAT


async def bride_get_viloyat_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Boshqa viloyatga ketishga rozimisiz?", reply_markup=yes_no_manual_back_keyboard("bv"))
        return BRIDE_VILOYAT
    context.user_data["viloyat_rozi"] = update.message.text
    await update.message.reply_text("Kuyov ajrashgan bo'lsa rozimisiz?", reply_markup=yes_no_manual_back_keyboard("bka"))
    return BRIDE_KUYOV_AJRASHGAN


async def bride_get_kuyov_ajrashgan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "bka_back":
        await query.edit_message_text("Boshqa viloyatga ketishga rozimisiz?", reply_markup=yes_no_manual_back_keyboard("bv"))
        return BRIDE_VILOYAT
    if data == "bka_manual":
        await query.edit_message_text("Kuyov ajrashgan bo'lsa rozimisiz?")
        await query.message.reply_text("Javobni yozing ✍️", reply_markup=back_button_reply())
        return BRIDE_KUYOV_AJRASHGAN_MANUAL
    context.user_data["kuyov_ajrashgan"] = data[4:]
    await query.edit_message_text("Ikkinchi ro'zg'orga rozi bo'lishingiz mumkinmi?", reply_markup=yes_no_manual_back_keyboard("bir"))
    return BRIDE_IKKINCHI_ROZGOR


async def bride_get_kuyov_ajrashgan_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing yoki \"Qo'lda yozish\" tugmasini bosing.")
    return BRIDE_KUYOV_AJRASHGAN


async def bride_get_kuyov_ajrashgan_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Kuyov ajrashgan bo'lsa rozimisiz?", reply_markup=yes_no_manual_back_keyboard("bka"))
        return BRIDE_KUYOV_AJRASHGAN
    context.user_data["kuyov_ajrashgan"] = update.message.text
    await update.message.reply_text("Ikkinchi ro'zg'orga rozi bo'lishingiz mumkinmi?", reply_markup=yes_no_manual_back_keyboard("bir"))
    return BRIDE_IKKINCHI_ROZGOR


async def bride_get_ikkinchi_rozgor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "bir_back":
        await query.edit_message_text("Kuyov ajrashgan bo'lsa rozimisiz?", reply_markup=yes_no_manual_back_keyboard("bka"))
        return BRIDE_KUYOV_AJRASHGAN
    if data == "bir_manual":
        await query.edit_message_text("Ikkinchi ro'zg'orga rozi bo'lishingiz mumkinmi?")
        await query.message.reply_text("Javobni yozing ✍️", reply_markup=back_button_reply())
        return BRIDE_IKKINCHI_ROZGOR_MANUAL
    context.user_data["ikkinchi_rozgor"] = data[4:]
    await query.edit_message_text("Kuyov yoshi chegarasini yozing?")
    return BRIDE_KUYOV_YOSH


async def bride_get_ikkinchi_rozgor_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing yoki \"Qo'lda yozish\" tugmasini bosing.")
    return BRIDE_IKKINCHI_ROZGOR


async def bride_get_ikkinchi_rozgor_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Ikkinchi ro'zg'orga rozi bo'lishingiz mumkinmi?", reply_markup=yes_no_manual_back_keyboard("bir"))
        return BRIDE_IKKINCHI_ROZGOR
    context.user_data["ikkinchi_rozgor"] = update.message.text
    await update.message.reply_text("Kuyov yoshi chegarasini yozing?", reply_markup=back_button_reply())
    return BRIDE_KUYOV_YOSH


async def bride_get_kuyov_yosh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Ikkinchi ro'zg'orga rozi bo'lishingiz mumkinmi?", reply_markup=yes_no_manual_back_keyboard("bir"))
        return BRIDE_IKKINCHI_ROZGOR
    context.user_data["kuyov_yosh"] = update.message.text
    await update.message.reply_text("Kuyovga talabingizni yozing?", reply_markup=back_button_reply())
    return BRIDE_KUYOV_TALAB


async def bride_get_kuyov_talab(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Kuyov yoshi chegarasini yozing?", reply_markup=back_button_reply())
        return BRIDE_KUYOV_YOSH
    context.user_data["kuyov_talab"] = update.message.text
    await update.message.reply_text(
        "Nomzodlar siz bilan bog'lanish ✍️ uchun Username (Foydalanuvchi nomi) ni yozing? (masalan: @username)",
        reply_markup=back_button_reply()
    )
    return BRIDE_USERNAME


async def bride_get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Kuyovga talabingizni yozing?", reply_markup=back_button_reply())
        return BRIDE_KUYOV_TALAB
    context.user_data["username"] = update.message.text
    contact_button = KeyboardButton("📱 Kontakt yuborish", request_contact=True)
    back_btn = KeyboardButton("⬅️ Oldingi savolga qaytish")
    reply_markup = ReplyKeyboardMarkup([[contact_button], [back_btn]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Anketani yakunlash uchun pastdagi \"Kontakt yuborish\" tugmasi orqali kontaktingizni yuboring.",
        reply_markup=reply_markup,
    )
    return CONTACT


# ==================== GROOM FLOW ====================

async def groom_get_marital(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "gm_back":
        await send_location_question(query, edit=True)
        return LOCATION
    context.user_data["marital_status"] = data[3:]
    await query.edit_message_text("Ish joyingiz haqida yozing?")
    return GROOM_JOB


async def groom_get_marital_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing.")
    return GROOM_MARITAL


async def groom_get_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Turmushdagi holatingiz?", reply_markup=groom_marital_keyboard())
        return GROOM_MARITAL
    context.user_data["job"] = update.message.text
    await update.message.reply_text("Kelin ajrashgan bo'lsa bo'ladimi?", reply_markup=yes_no_manual_back_keyboard("gka"))
    return GROOM_KELIN_AJRASHGAN


async def groom_get_kelin_ajrashgan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "gka_back":
        await query.edit_message_text("Ish joyingiz haqida yozing?")
        return GROOM_JOB
    if data == "gka_manual":
        await query.edit_message_text("Kelin ajrashgan bo'lsa bo'ladimi?")
        await query.message.reply_text("Javobni yozing ✍️", reply_markup=back_button_reply())
        return GROOM_KELIN_AJRASHGAN_MANUAL
    context.user_data["kelin_ajrashgan"] = data[4:]
    await query.edit_message_text("O'zingiz haqingizda yozing?")
    return GROOM_HAQIDA


async def groom_get_kelin_ajrashgan_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing yoki \"Qo'lda yozish\" tugmasini bosing.")
    return GROOM_KELIN_AJRASHGAN


async def groom_get_kelin_ajrashgan_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Kelin ajrashgan bo'lsa bo'ladimi?", reply_markup=yes_no_manual_back_keyboard("gka"))
        return GROOM_KELIN_AJRASHGAN
    context.user_data["kelin_ajrashgan"] = update.message.text
    await update.message.reply_text("O'zingiz haqingizda yozing?", reply_markup=back_button_reply())
    return GROOM_HAQIDA


async def groom_get_haqida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Kelin ajrashgan bo'lsa bo'ladimi?", reply_markup=yes_no_manual_back_keyboard("gka"))
        return GROOM_KELIN_AJRASHGAN
    context.user_data["about_groom"] = update.message.text
    await update.message.reply_text("Kelinga talabingiz?", reply_markup=back_button_reply())
    return GROOM_KELIN_TALAB


async def groom_get_kelin_talab(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("O'zingiz haqingizda yozing?", reply_markup=back_button_reply())
        return GROOM_HAQIDA
    context.user_data["kelin_talab"] = update.message.text
    await update.message.reply_text(
        "Nomzodlar siz bilan bog'lanish ✍️ uchun Username (Foydalanuvchi nomi) ni yozing? (masalan: @username)",
        reply_markup=back_button_reply()
    )
    return GROOM_USERNAME


async def groom_get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "⬅️ Oldingi savolga qaytish":
        await update.message.reply_text("Kelinga talabingiz?", reply_markup=back_button_reply())
        return GROOM_KELIN_TALAB
    context.user_data["username"] = update.message.text
    contact_button = KeyboardButton("📱 Kontakt yuborish", request_contact=True)
    back_btn = KeyboardButton("⬅️ Oldingi savolga qaytish")
    reply_markup = ReplyKeyboardMarkup([[contact_button], [back_btn]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Anketani yakunlash uchun pastdagi \"Kontakt yuborish\" tugmasi orqali kontaktingizni yuboring.",
        reply_markup=reply_markup,
    )
    return CONTACT


# ==================== CONTACT & FINISH ====================

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Orqaga qaytish tekshiruvi
    if update.message.text and update.message.text == "⬅️ Oldingi savolga qaytish":
        role = context.user_data.get("role")
        if role == "bride":
            await update.message.reply_text(
                "Nomzodlar siz bilan bog'lanish ✍️ uchun Username (Foydalanuvchi nomi) ni yozing? (masalan: @username)",
                reply_markup=back_button_reply()
            )
            return BRIDE_USERNAME
        else:
            await update.message.reply_text(
                "Nomzodlar siz bilan bog'lanish ✍️ uchun Username (Foydalanuvchi nomi) ni yozing? (masalan: @username)",
                reply_markup=back_button_reply()
            )
            return GROOM_USERNAME

    if not update.message.contact:
        contact_button = KeyboardButton("📱 Kontakt yuborish", request_contact=True)
        back_btn = KeyboardButton("⬅️ Oldingi savolga qaytish")
        reply_markup = ReplyKeyboardMarkup([[contact_button], [back_btn]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "❌ Iltimos, pastdagi \"Kontakt yuborish\" tugmasini bosing.",
            reply_markup=reply_markup
        )
        return CONTACT

    contact = update.message.contact
    contact_message_id = update.message.message_id
    chat_id = update.effective_chat.id
    role = context.user_data.get("role")
    d = context.user_data

    if role == "bride":
        survey_text = (
            "#Kelinlikga nomzod #kelin\n"
            "\n"
            f"- Ismi:  {d.get('name', '')}\n"
            f"- Yoshi: {d.get('age', '')}\n"
            f"- Bo'yi: {d.get('height', '')}\n"
            f"- Vazni: {d.get('weight', '')}\n"
            f"- Millati: {d.get('nationality', '')}\n"
            f"- Yashash joyi:  {d.get('location', '')}\n"
            f"- Ish joyi:  {d.get('job', '')}\n"
            f"- Turmushdagi xolati: {d.get('marital_status', '')}\n"
            f"- Ajrashgan bo'lsa farzandi: {d.get('children', '')}\n"
            f"- Boshqa viloyatga ketishga rozimi: {d.get('viloyat_rozi', '')}\n"
            f"- Kuyov ajrashgan bo'lsa rozimisiz: {d.get('kuyov_ajrashgan', '')}\n"
            "\n"
            f"- Ikkinchi ro'zg'orga rozi bo'lishingiz mumkinmi: {d.get('ikkinchi_rozgor', '')}\n"
            "\n"
            f"- Kuyov yoshi chegarasi: {d.get('kuyov_yosh', '')}\n"
            "\n"
            f"🤵‍♂️ Kuyovga talab: {d.get('kuyov_talab', '')}\n"
            "\n"
            f"✍🏻 Murojat uchun: {d.get('username', '')}"
        )
        channel_id = BRIDE_CHANNEL_ID
    else:
        survey_text = (
            "#Kuyovlikka nomzod #kuyov\n"
            "\n"
            f"- Ismi: {d.get('name', '')}\n"
            f"- Yoshi: {d.get('age', '')}\n"
            f"- Bo'yi: {d.get('height', '')}\n"
            f"- Vazni: {d.get('weight', '')}\n"
            f"- Millati: {d.get('nationality', '')}\n"
            f"- Yashash joyi: {d.get('location', '')}\n"
            f"- Turmushdagi xolati: {d.get('marital_status', '')}\n"
            f"- Ish joyi: {d.get('job', '')}\n"
            f"- Kelin ajrashgan bo'lsa bo'ladimi: {d.get('kelin_ajrashgan', '')}\n"
            "\n"
            f"🤵🏻Kuyov haqida: {d.get('about_groom', '')}\n"
            "\n"
            f"👰‍♀️Kelinga talab: {d.get('kelin_talab', '')}\n"
            "\n"
            f"✍🏻 Murojat uchun: {d.get('username', '')}"
        )
        channel_id = GROOM_CHANNEL_ID

    # Send anketa to user
    await update.message.reply_text(survey_text, reply_markup=ReplyKeyboardRemove())

    # Send anketa to channel
    try:
        await context.bot.send_message(chat_id=channel_id, text=survey_text)
        # Forward contact to channel
        await context.bot.forward_message(
            chat_id=channel_id,
            from_chat_id=chat_id,
            message_id=contact_message_id
        )
    except Exception as e:
        logger.error(f"Kanalga yuborishda xatolik: {e}")

    # Send confirmation message to user
    await update.message.reply_text(
        "Sizning anketangiz tayyor. Kanal admiga yuborildi. Iltimos kanal adminidan aniqlik kiritib oling."
    )

    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Anketa to'ldirish bekor qilindi.", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END


# ==================== SELECTING_ROLE da matn yozilsa ====================
async def selecting_role_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Iltimos, yuqoridagi tugmalardan birini bosing: 👰‍♂️Kelin nomzod yoki 🤵‍♂️ Kuyov nomzod")
    return SELECTING_ROLE


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ROLE: [
                CallbackQueryHandler(select_role),
                MessageHandler(filters.TEXT & ~filters.COMMAND, selecting_role_text),
            ],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
            NATIONALITY: [
                CallbackQueryHandler(get_nationality),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_nationality_text),
            ],
            NATIONALITY_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_nationality_manual)],
            LOCATION: [
                CallbackQueryHandler(get_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_location_text),
            ],
            LOCATION_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location_manual)],
            # Bride flow
            BRIDE_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_job)],
            BRIDE_MARITAL: [
                CallbackQueryHandler(bride_get_marital),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_marital_text),
            ],
            BRIDE_CHILDREN: [
                CallbackQueryHandler(bride_get_children),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_children_text),
            ],
            BRIDE_VILOYAT: [
                CallbackQueryHandler(bride_get_viloyat),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_viloyat_text),
            ],
            BRIDE_VILOYAT_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_viloyat_manual)],
            BRIDE_KUYOV_AJRASHGAN: [
                CallbackQueryHandler(bride_get_kuyov_ajrashgan),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_kuyov_ajrashgan_text),
            ],
            BRIDE_KUYOV_AJRASHGAN_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_kuyov_ajrashgan_manual)],
            BRIDE_IKKINCHI_ROZGOR: [
                CallbackQueryHandler(bride_get_ikkinchi_rozgor),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_ikkinchi_rozgor_text),
            ],
            BRIDE_IKKINCHI_ROZGOR_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_ikkinchi_rozgor_manual)],
            BRIDE_KUYOV_YOSH: [MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_kuyov_yosh)],
            BRIDE_KUYOV_TALAB: [MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_kuyov_talab)],
            BRIDE_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, bride_get_username)],
            # Groom flow
            GROOM_MARITAL: [
                CallbackQueryHandler(groom_get_marital),
                MessageHandler(filters.TEXT & ~filters.COMMAND, groom_get_marital_text),
            ],
            GROOM_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, groom_get_job)],
            GROOM_KELIN_AJRASHGAN: [
                CallbackQueryHandler(groom_get_kelin_ajrashgan),
                MessageHandler(filters.TEXT & ~filters.COMMAND, groom_get_kelin_ajrashgan_text),
            ],
            GROOM_KELIN_AJRASHGAN_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, groom_get_kelin_ajrashgan_manual)],
            GROOM_HAQIDA: [MessageHandler(filters.TEXT & ~filters.COMMAND, groom_get_haqida)],
            GROOM_KELIN_TALAB: [MessageHandler(filters.TEXT & ~filters.COMMAND, groom_get_kelin_talab)],
            GROOM_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, groom_get_username)],
            # Contact
            CONTACT: [
                MessageHandler(filters.CONTACT, get_contact),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact),
            ],
        },
        fallbacks=[CommandHandler("start", start), CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
