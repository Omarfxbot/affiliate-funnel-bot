import os
import psycopg2

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

EXNESS_LINK = "https://one.exnessonelink.com/a/zi8w32eknv"
ROBO_LINK = "https://my.roboforex.com/en/?a=omawl"

# روابط الشرح
EXNESS_TUTORIAL = "https://t.me/+z5iRMblllboxYWNk"
ROBO_TUTORIAL = "https://t.me/+68YvPcWphtE3ZGM0"

ADMIN_USERNAME = "@OmartradingAux"


# -------- DATABASE --------

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS signals (
id SERIAL PRIMARY KEY,
symbol TEXT,
direction TEXT,
result TEXT,
profit FLOAT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# -------- START --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [KeyboardButton("🔥 منصة احترافية Exness")],
        [KeyboardButton("🎁 RoboForex Bonus 30$ + 10$")],
        [KeyboardButton("✅ سجلت بالفعل")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    text = """
👋 مرحبا

باغي إشارات GOLD جاهزة؟ 📈

كنقرا المارشي وكنعطيك فرص واضحة 🤖 AI BOT

باش تبدأ 👇
اختار واحد من المنصات وسجل

ومن بعد رجع واضغط:
✅ سجلت بالفعل
"""

    await update.message.reply_text(text, reply_markup=reply_markup)


# -------- HANDLER --------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if "Exness" in text:

        await update.message.reply_text(
            f"""
🔥 اختيار احترافي

📥 التسجيل:
{EXNESS_LINK}

📺 شرح التسجيل خطوة بخطوة:
{EXNESS_TUTORIAL}

ومن بعد رجع واضغط:
✅ سجلت بالفعل
"""
        )

    elif "RoboForex" in text:

        await update.message.reply_text(
            f"""
🎁 تبدأ ب 10$ فقط
وتاخد Bonus 30$

📥 التسجيل:
{ROBO_LINK}

📺 شرح التسجيل:
{ROBO_TUTORIAL}

ومن بعد رجع واضغط:
✅ سجلت بالفعل
"""
        )

    elif "سجلت بالفعل" in text:

        await update.message.reply_text(
            f"""
ممتاز 👌

تواصل معايا هنا باش نتأكد من التسجيل 👇

👉 {ADMIN_USERNAME}

🔒 ومن بعد نعطيك الولوج لقناة VIP
"""
        )


# -------- DASHBOARD --------

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cur.execute("SELECT COUNT(*) FROM signals")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM signals WHERE result='WIN'")
    wins = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM signals WHERE result='LOSS'")
    loss = cur.fetchone()[0]

    winrate = 0
    if total > 0:
        winrate = round((wins / total) * 100, 2)

    cur.execute("SELECT COALESCE(SUM(profit),0) FROM signals")
    profit = cur.fetchone()[0]

    text = f"""
📊 AI GOLD BOT DASHBOARD

Signals: {total}
Wins: {wins}
Loss: {loss}

Winrate: {winrate} %
Profit: {profit} $

Status: Running
"""

    await update.message.reply_text(text)


# -------- RUN --------

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("dashboard", dashboard))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Affiliate Funnel Bot Running")

app.run_polling(drop_pending_updates=True)
