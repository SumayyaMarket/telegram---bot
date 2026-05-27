import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

TOKEN = "8637196168:AAG78Jnvl9h0-jCym6oBH9NzesSpLJxm4P0"
ADMIN_ID = 8650564088

YETKAZIB_BERISH_NARXI = 15000
ISH_VAQTI = "09:00 - 21:00"
DOKON_MANZILI = "Guliston shahar, Ankologiya Markazi yonida"
TELEFON = "+998 XX XXX XX XX"

KATEGORIYA, MAHSULOT, MIQDOR, MANZIL, TASDIQLASH = range(5)
savatchalar = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KATEGORIYALAR = {
    "🍞 Non": {
        "Oq non": 5000,
    },
    "🍎 Mevalar": {
        "Olma (1 kg)": 35000,
        "Banan (1 kg)": 27000,
        "Apelsin (1 kg)": 35000,
        "Anor (1 kg)": 40000,
        "Nok (1 kg)": 28000,
        "Kivi (1 kg)": 35000,
        "Limon (1 kg)": 65000,
    },
    "💧 Suvlar va Ichimliklar": {
        "Toza suv (0.5L)": 3000,
        "Toza suv (1L)": 4000,
        "Toza suv (1.5L)": 6000,
        "Toza suv (5L)": 7000,
        "Toza suv (10L)": 10000,
        "Flesh (1L)": 12000,
        "Gorilla (1L)": 13000,
        "Moxito (1L)": 13000,
        "Kola (0.5L)": 7000,
        "Kola (1L)": 12000,
        "Kola (1.5L)": 15000,
        "Kola (2L)": 20000,
        "Fanta (0.5L)": 7000,
        "Fanta (1L)": 12000,
        "Fanta (1.5L)": 15000,
        "Fanta (2L)": 20000,
    },
    "🥛 Sut Mahsulotlari": {
        "Kefir (1L)": 8000,
        "Yogurt (1 dona)": 7000,
        "Yogurt baklashka": 12000,
        "Qaymoq": 16000,
        "Sariyog' idishcha": 15000,
    },
    "🌭 Kolbasa va Sir": {
        "Varyonniy (1 kg)": 75000,
        "Kapchonniy (1 kg)": 90000,
        "Vakum (1 ta)": 25000,
        "Krakuskiy (1 dona)": 8000,
        "Sir Prezident (1 kg)": 85000,
        "Doktor (1 kg)": 80000,
    },
    "🍪 Pishiriqlar": {
        "Konteyner pishiriq (1 dona)": 28000,
        "Bo'lichka pachka": 12000,
        "Pryanik (1 kg)": 35000,
        "Yubileyni (1 kg)": 28000,
        "Padushka (1 kg)": 30000,
        "Tvarojniy (1 kg)": 65000,
        "Bo'lichka (1 kg)": 40000,
    },
}

def asosiy_menyu():
    tugmalar = [
        ["🛒 Buyurtma berish", "🛍 Savatcham"],
        ["📋 Kategoriyalar", "ℹ️ Ma'lumot"],
        ["📞 Bog'lanish", "🕐 Ish vaqti"]
    ]
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)

def kategoriya_menyu():
    tugmalar = [[k] for k in KATEGORIYALAR.keys()]
    tugmalar.append(["🔙 Orqaga"])
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)

def mahsulot_menyu(kategoriya):
    mahsulotlar = KATEGORIYALAR.get(kategoriya, {})
    tugmalar = []
    for nom, narx in mahsulotlar.items():
        tugmalar.append([f"{nom} - {narx:,} so'm"])
    tugmalar.append(["🔙 Orqaga"])
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)

def savatcha_matni(user_id):
    if user_id not in savatchalar or not savatchalar[user_id]:
        return "🛍 Savatchingiz bo'sh"
    matn = "🛍 *Savatchingiz:*\n\n"
    jami = 0
    for mahsulot, (narx, miqdor) in savatchalar[user_id].items():
        summa = narx * miqdor
        jami += summa
        matn += f"• {mahsulot} x{miqdor} = {summa:,} so'm\n"
    matn += f"\n💰 *Jami: {jami:,} so'm*"
    matn += f"\n🚚 *Yetkazib berish: {YETKAZIB_BERISH_NARXI:,} so'm*"
    matn += f"\n\n💳 *Umumiy: {jami + YETKAZIB_BERISH_NARXI:,} so'm*"
    return matn

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    matn = (
        f"🌸 Assalomu aleykum, *{user.first_name}*!\n\n"
        f"🏪 *SUMAYYA MARKET* botiga xush kelibsiz!\n\n"
        f"✅ Sifatli mahsulotlar\n"
        f"🚚 Yetkazib berish: *{YETKAZIB_BERISH_NARXI:,} so'm*\n"
        f"🕐 Ish vaqti: *{ISH_VAQTI}*\n"
        f"📍 *{DOKON_MANZILI}*\n\n"
        f"Buyurtma berish uchun *'🛒 Buyurtma berish'* tugmasini bosing!"
    )
    await update.message.reply_text(matn, parse_mode="Markdown", reply_markup=asosiy_menyu())

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = (
        f"ℹ️ *SUMAYYA MARKET haqida*\n\n"
        f"📍 Manzil: {DOKON_MANZILI}\n"
        f"📞 Telefon: {TELEFON}\n"
        f"🕐 Ish vaqti: {ISH_VAQTI}\n"
        f"🚚 Yetkazib berish: {YETKAZIB_BERISH_NARXI:,} so'm\n\n"
        f"🌸 Sifatli mahsulotlar, qulay narxlar!"
    )
    await update.message.reply_text(matn, parse_mode="Markdown", reply_markup=asosiy_menyu())

async def kategoriyalar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 *Kategoriyani tanlang:*", parse_mode="Markdown", reply_markup=kategoriya_menyu())
    return KATEGORIYA

async def savatcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    matn = savatcha_matni(user_id)
    if user_id in savatchalar and savatchalar[user_id]:
        tugmalar = [["✅ Buyurtmani rasmiylashtirish"], ["🗑 Savatchani tozalash"], ["🔙 Orqaga"]]
        markup = ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
    else:
        markup = asosiy_menyu()
    await update.message.reply_text(matn, parse_mode="Markdown", reply_markup=markup)

async def kategoriya_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    if matn == "🔙 Orqaga":
        await update.message.reply_text("Asosiy menyu:", reply_markup=asosiy_menyu())
        return ConversationHandler.END
    if matn in KATEGORIYALAR:
        context.user_data["kategoriya"] = matn
        await update.message.reply_text(f"*{matn}*\n\nMahsulotni tanlang:", parse_mode="Markdown", reply_markup=mahsulot_menyu(matn))
        return MAHSULOT
    await update.message.reply_text("Kategoriyani tanlang:", reply_markup=kategoriya_menyu())
    return KATEGORIYA

async def mahsulot_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    if matn == "🔙 Orqaga":
        await update.message.reply_text("Kategoriyani tanlang:", reply_markup=kategoriya_menyu())
        return KATEGORIYA
    if " - " in matn:
        mahsulot_nomi = matn.split(" - ")[0]
        kategoriya = context.user_data.get("kategoriya")
        if kategoriya and mahsulot_nomi in KATEGORIYALAR.get(kategoriya, {}):
            narx = KATEGORIYALAR[kategoriya][mahsulot_nomi]
            context.user_data["mahsulot"] = mahsulot_nomi
            context.user_data["narx"] = narx
            tugmalar = [["1", "2", "3"], ["4", "5", "10"], ["🔙 Orqaga"]]
            await update.message.reply_text(
                f"*{mahsulot_nomi}*\nNarxi: {narx:,} so'm\n\nNechtasini olasiz?",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
            )
            return MIQDOR
    await update.message.reply_text("Mahsulotni tanlang:", reply_markup=mahsulot_menyu(context.user_data.get("kategoriya", "")))
    return MAHSULOT

async def miqdor_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    if matn == "🔙 Orqaga":
        kategoriya = context.user_data.get("kategoriya")
        await update.message.reply_text("Mahsulotni tanlang:", reply_markup=mahsulot_menyu(kategoriya))
        return MAHSULOT
    try:
        miqdor = int(matn)
        user_id = update.effective_user.id
        mahsulot = context.user_data["mahsulot"]
        narx = context.user_data["narx"]
        if user_id not in savatchalar:
            savatchalar[user_id] = {}
        savatchalar[user_id][mahsulot] = (narx, miqdor)
        tugmalar = [["🛒 Yana mahsulot qo'shish"], ["🛍 Savatcham ko'rish"], ["✅ Buyurtmani rasmiylashtirish"]]
        await update.message.reply_text(
            f"✅ *{mahsulot}* x{miqdor} savatchaga qo'shildi!",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
        )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Iltimos, raqam kiriting (1, 2, 3...)")
        return MIQDOR

async def manzil_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in savatchalar or not savatchalar[user_id]:
        await update.message.reply_text("Savatchingiz bo'sh! Avval mahsulot tanlang.", reply_markup=asosiy_menyu())
        return ConversationHandler.END
    tugma = KeyboardButton("📍 Manzilimni yuborish", request_location=True)
    markup = ReplyKeyboardMarkup([[tugma], ["✍️ Manzilni yozib yuborish"], ["🔙 Orqaga"]], resize_keyboard=True)
    await update.message.reply_text(
        "📍 *Yetkazib berish manzilini yuboring:*",
        parse_mode="Markdown",
        reply_markup=markup
    )
    return MANZIL

async def manzil_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.location:
        context.user_data["manzil"] = f"lat={update.message.location.latitude}, lon={update.message.location.longitude}"
        manzil_matn = "📍 Joylashuv yuborildi"
    else:
        manzil_matn = update.message.text
        context.user_data["manzil"] = manzil_matn
    savatcha_m = savatcha_matni(user_id)
    jami = sum(n * m for n, m in savatchalar[user_id].values())
    matn = f"{savatcha_m}\n\n📍 *Manzil:* {manzil_matn}\n\nBuyurtmani tasdiqlaysizmi?"
    tugmalar = [["✅ Tasdiqlash", "❌ Bekor qilish"]]
    await update.message.reply_text(matn, parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(tugmalar, resize_keyboard=True))
    return TASDIQLASH

async def buyurtma_tasdiqlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = update.effective_user
    matn = update.message.text
    if matn == "✅ Tasdiqlash":
        manzil = context.user_data.get("manzil", "Noma'lum")
        savatcha_m = savatcha_matni(user_id)
        jami = sum(n * m for n, m in savatchalar[user_id].values())
        await update.message.reply_text(
            f"🎉 *Buyurtmangiz qabul qilindi!*\n\n⏰ Yetkazib berish: *30-60 daqiqa*\n📞 Operator siz bilan bog'lanadi\n\nRahmat! 🌸",
            parse_mode="Markdown", reply_markup=asosiy_menyu()
        )
        admin_matn = (
            f"🔔 *YANGI BUYURTMA!*\n\n"
            f"👤 Mijoz: {user.first_name} {user.last_name or ''}\n"
            f"📱 Username: @{user.username or 'yoq'}\n"
            f"🆔 ID: {user_id}\n\n"
            f"{savatcha_m}\n\n"
            f"📍 Manzil: {manzil}\n"
            f"💰 Umumiy: {jami + YETKAZIB_BERISH_NARXI:,} so'm"
        )
        try:
            await context.bot.send_message(ADMIN_ID, admin_matn, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Admin xabari yuborilmadi: {e}")
        savatchalar[user_id] = {}
    else:
        await update.message.reply_text("❌ Buyurtma bekor qilindi.", reply_markup=asosiy_menyu())
    return ConversationHandler.END

async def savatchani_tozalash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    savatchalar[user_id] = {}
    await update.message.reply_text("🗑 Savatcha tozalandi!", reply_markup=asosiy_menyu())

async def umumiy_xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    if matn in ["🛒 Buyurtma berish", "📋 Kategoriyalar", "🛒 Yana mahsulot qo'shish"]:
        await update.message.reply_text("Kategoriyani tanlang:", reply_markup=kategoriya_menyu())
        return KATEGORIYA
    elif matn in ["🛍 Savatcham", "🛍 Savatcham ko'rish"]:
        await savatcha(update, context)
    elif matn == "✅ Buyurtmani rasmiylashtirish":
        await manzil_olish(update, context)
        return MANZIL
    elif matn == "🗑 Savatchani tozalash":
        await savatchani_tozalash(update, context)
    elif matn == "ℹ️ Ma'lumot":
        await info(update, context)
    elif matn == "📞 Bog'lanish":
        await update.message.reply_text(
            f"📞 *Bog'lanish:*\n\n📱 Telefon: {TELEFON}\n📍 Manzil: {DOKON_MANZILI}\n🕐 Ish vaqti: {ISH_VAQTI}",
            parse_mode="Markdown", reply_markup=asosiy_menyu()
        )
    elif matn == "🕐 Ish vaqti":
        await update.message.reply_text(
            f"🕐 *Ish vaqtimiz:*\n\nHar kuni\n*{ISH_VAQTI}*\n\n🌸",
            parse_mode="Markdown", reply_markup=asosiy_menyu()
        )
    else:
        await update.message.reply_text("Iltimos, tugmalardan birini tanlang:", reply_markup=asosiy_menyu())

def main():
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^(🛒 Buyurtma berish|📋 Kategoriyalar|🛒 Yana mahsulot qo'shish)$"), kategoriyalar),
            MessageHandler(filters.Regex("^✅ Buyurtmani rasmiylashtirish$"), manzil_olish),
        ],
        states={
            KATEGORIYA: [MessageHandler(filters.TEXT & ~filters.COMMAND, kategoriya_tanlash)],
            MAHSULOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, mahsulot_tanlash)],
            MIQDOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, miqdor_tanlash)],
            MANZIL: [
                MessageHandler(filters.LOCATION, manzil_qabul),
                MessageHandler(filters.TEXT & ~filters.COMMAND, manzil_qabul),
            ],
            TASDIQLASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, buyurtma_tasdiqlash)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, umumiy_xabar))
    print("✅ SUMAYYA MARKET boti ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
