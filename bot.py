from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ===== Data kategori =====
kategori = {
    "order": 0,
    "bensin": 0,
    "makan": 0,
    "parkir": 0,
    "servis": 0,
    "jajan": 0
}

# ===== Keyboard menu =====
menu = [
    ["🚕 Order Ojol", "⛽ Bensin"],
    ["🍜 Makan", "🅿️ Parkir"],
    ["🔧 Servis", "🛍️ Jajan"],
    ["📊 Saldo"]
]

keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)

# ===== State sementara =====
state = {}

# ===== Start command =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 BOT KEUANGAN OJOL\n\nPilih menu:",
        reply_markup=keyboard
    )

# ===== Handler pesan =====
async def pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat_id
    text = update.message.text

    # Pilihan kategori
    if text == "🚕 Order Ojol":
        state[user] = "order"
        await update.message.reply_text("Masukkan jumlah order:")

    elif text == "⛽ Bensin":
        state[user] = "bensin"
        await update.message.reply_text("Masukkan biaya bensin:")

    elif text == "🍜 Makan":
        state[user] = "makan"
        await update.message.reply_text("Masukkan biaya makan:")

    elif text == "🅿️ Parkir":
        state[user] = "parkir"
        await update.message.reply_text("Masukkan biaya parkir:")

    elif text == "🔧 Servis":
        state[user] = "servis"
        await update.message.reply_text("Masukkan biaya servis:")

    elif text == "🛍️ Jajan":
        state[user] = "jajan"
        await update.message.reply_text("Masukkan biaya jajan:")

    # Lihat saldo
    elif text == "📊 Saldo":
        total_keluar = kategori["bensin"] + kategori["makan"] + kategori["parkir"] + kategori["servis"] + kategori["jajan"]
        saldo = kategori["order"] - total_keluar

        await update.message.reply_text(
f"""📊 REKAP KEUANGAN

🚕 Order : {kategori["order"]}
⛽ Bensin : {kategori["bensin"]}
🍜 Makan : {kategori["makan"]}
🅿️ Parkir : {kategori["parkir"]}
🔧 Servis : {kategori["servis"]}
🛍️ Jajan : {kategori["jajan"]}

💰 Saldo Bersih : {saldo}"""
        )

    # Input nominal
    else:
        if user in state and state[user] is not None:
            try:
                jumlah = int(text)
                kategori[state[user]] += jumlah

                total_keluar = kategori["bensin"] + kategori["makan"] + kategori["parkir"] + kategori["servis"] + kategori["jajan"]
                saldo = kategori["order"] - total_keluar

                await update.message.reply_text(
f"""✅ Data tersimpan

📊 Saldo terbaru

🚕 Order : {kategori["order"]}
⛽ Bensin : {kategori["bensin"]}
🍜 Makan : {kategori["makan"]}
🅿️ Parkir : {kategori["parkir"]}
🔧 Servis : {kategori["servis"]}
🛍️ Jajan : {kategori["jajan"]}

💰 Saldo : {saldo}"""
                )
                state[user] = None
            except ValueError:
                await update.message.reply_text("❌ Masukkan angka saja!")
        else:
            await update.message.reply_text("Pilih menu dulu!")

# ===== Main =====
if __name__ == "__main__":
    print("Bot keuangan ojol aktif...")
    app = ApplicationBuilder().token("8482263728:AAEJI2AozPQZDmUNNmpEYr2_6MOkRDFD_Vw").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, pesan))
    app.run_polling()
