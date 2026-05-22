# =========================
# MAIN.PY
# =========================

import telebot
import json
import random
import time

from admin import *
from shop import *

# =========================
# BOT INFO
# =========================

TOKEN = "8798016129:AAFsInsy6oeOQMeTLrcOtHl7RqgOYD4cfEc"

ADMIN_ID = 7553598484

BOT_USERNAME = "Serv46_bot"

bot = telebot.TeleBot(TOKEN)

DB_FILE = "db.json"

# =========================
# BUTTON COLORS
# =========================

PRIMARY = "primary"
SUCCESS = "success"
DANGER = "danger"

# =========================
# BUTTON
# =========================

def btn(text,data,style=PRIMARY):

    return telebot.types.InlineKeyboardButton(

        text=text,

        callback_data=data,

        style=style

    )

# =========================
# LOAD DB
# =========================

def load_db():

    try:

        with open(DB_FILE,"r",encoding="utf-8") as f:

            return json.load(f)

    except:

        return {

            "users":{},
            "products":{},
            "categories":{},
            "orders":[],

            "settings":{

                "currency_name":"MineCoin",

                "mine_min":5,
                "mine_max":20,

                "mine_cooldown":1800,

                "daily_reward":25,

                "invite_reward":10,

                "discount":0,

                "tax":0

            }

        }

# =========================
# SAVE DB
# =========================

def save_db(db):

    with open(DB_FILE,"w",encoding="utf-8") as f:

        json.dump(
            db,
            f,
            ensure_ascii=False,
            indent=2
        )

# =========================
# CREATE USER
# =========================

def create_user(db,uid):

    uid = str(uid)

    if uid not in db["users"]:

        db["users"][uid] = {

            "mc":0,

            "mine":0,

            "daily":0,

            "invites":0,

            "joined":False,

            "level":1,

            "xp":0

        }

# =========================
# TRANSFER STEPS
# =========================

transfer_steps = {}

# =========================
# MAIN MENU
# =========================

def main_menu(uid):

    kb = telebot.types.InlineKeyboardMarkup(
        row_width=2
    )

    kb.add(

        btn(
            "المنتجات",
            "categories",
            PRIMARY
        )

    )

    kb.add(

        btn(
            "تجميع MineCoin",
            "collect",
            SUCCESS
        )

    )

    kb.add(

        btn(
            "رصيدي",
            "balance",
            PRIMARY
        ),

        btn(
            "تحويل",
            "transfer",
            SUCCESS
        )

    )

    kb.add(

        btn(
            "المهام",
            "tasks",
            PRIMARY
        ),

        btn(
            "اليومي",
            "daily",
            SUCCESS
        )

    )

    kb.add(

        btn(
            "الدعوات",
            "invite",
            SUCCESS
        ),

        btn(
            "نسخ الرابط",
            "copy_invite",
            DANGER
        )

    )

    kb.add(

        btn(
            "الإحصائيات",
            "stats",
            PRIMARY
        ),

        btn(
            "المستوي",
            "level",
            SUCCESS
        )

    )

    kb.add(

        btn(
            "طلباتي",
            "orders",
            PRIMARY
        ),

        btn(
            "كوبون خصم",
            "coupon",
            SUCCESS
        )

    )

    kb.add(

        btn(
            "مراسلة المطور",
            "developer",
            DANGER
        )

    )

    # =========================
    # ADMIN BUTTON
    # =========================

    if uid == ADMIN_ID:

        kb.add(

            btn(
                "الإعدادات",
                "admin",
                DANGER
            )

        )

    return kb

# =========================
# COLLECT MENU
# =========================

def collect_menu():

    kb = telebot.types.InlineKeyboardMarkup(
        row_width=1
    )

    kb.add(

        btn(
            "التعدين",
            "mine",
            SUCCESS
        )

    )

    kb.add(

        btn(
            "الهدية اليومية",
            "daily",
            PRIMARY
        )

    )

    kb.add(

        btn(
            "المهام",
            "tasks",
            PRIMARY
        )

    )

    kb.add(

        btn(
            "الدعوات",
            "invite",
            SUCCESS
        )

    )

    kb.add(

        btn(
            "نسخ رابط الدعوة",
            "copy_invite",
            DANGER
        )

    )

    return kb

# =========================
# START
# =========================

@bot.message_handler(commands=["start"])
def start(msg):

    db = load_db()

    uid = msg.from_user.id

    create_user(db,uid)

    args = msg.text.split()

    # =========================
    # REFERRAL
    # =========================

    if len(args) > 1:

        inviter = args[1]

        if inviter != str(uid):

            if not db["users"][str(uid)]["joined"]:

                db["users"][str(uid)]["joined"] = True

                create_user(db,inviter)

                reward = db["settings"]["invite_reward"]

                db["users"][str(inviter)]["mc"] += reward

                db["users"][str(inviter)]["invites"] += 1

                bot.send_message(

                    inviter,

                    f"""
🎉 مستخدم جديد دخل من رابطك

💰 +{reward} MineCoin
"""

                )

    save_db(db)

    bot.send_message(

        msg.chat.id,

        f"""
🔥 أهلاً بك في متجر MineCoin

💰 اجمع العملات
🛍 اشتري منتجات
👥 ادعُ أصدقاءك
⛏ عدّن يومياً
🎁 خذ هدايا
""",

        reply_markup=main_menu(uid)

    )

# =========================
# CALLBACKS
# =========================

@bot.callback_query_handler(func=lambda c:True)
def callbacks(call):

    db = load_db()

    uid = call.from_user.id

    create_user(db,uid)

    user = db["users"][str(uid)]

    settings = db["settings"]

    now = int(time.time())

    data = call.data

    # =========================
    # COLLECT MENU
    # =========================

    if data == "collect":

        return bot.send_message(

            call.message.chat.id,

            """
💰 طرق التجميع المتاحة
""",

            reply_markup=collect_menu()

        )

    # =========================
    # TRANSFER
    # =========================

    elif data == "transfer":

        transfer_steps[uid] = True

        return bot.send_message(

            call.message.chat.id,

            """
💸 أرسل التحويل بالشكل التالي:

ايدي|عدد

مثال:
123456789|50
"""

        )

    # =========================
# MINE
# =========================

    # =========================
    # MINE
    # =========================

    elif data == "mine":

        if now - user["mine"] < settings["mine_cooldown"]:

            left = settings["mine_cooldown"] - (
                now - user["mine"]
            )

            return bot.answer_callback_query(
                call.id,
                f"⏳ انتظر {left} ثانية"
            )

        reward = random.randint(
            settings["mine_min"],
            settings["mine_max"]
        )

        user["mc"] += reward

        user["mine"] = now

        user["xp"] += reward

        if user["xp"] >= user["level"] * 100:

            user["xp"] = 0

            user["level"] += 1

            bot.send_message(
                call.message.chat.id,
                f"""
🏆 وصلت للمستوي {user['level']}
"""
            )

        save_db(db)

        return bot.send_message(
            call.message.chat.id,
            f"""
⛏ تم التعدين بنجاح

💰 +{reward} {settings['currency_name']}
"""
        )

# =========================
# DAILY
# =========================

    # =========================
    # DAILY
    # =========================

    elif data == "daily":

        if now - user["daily"] < 86400:

            return bot.answer_callback_query(

                call.id,

                "⏳ أخذت اليومي بالفعل"

            )

        reward = settings["daily_reward"]

        user["mc"] += reward

        user["daily"] = now

        save_db(db)

        bot.send_message(

            call.message.chat.id,

            f"""
🎁 تم استلام الهدية اليومية

💰 +{reward} {settings['currency_name']}
"""

        )

    # =========================
    # BALANCE
    # =========================

    elif data == "balance":

        bot.send_message(

            call.message.chat.id,

            f"""
💳 حسابك

💰 الرصيد:
{user['mc']} {settings['currency_name']}

🏆 المستوي:
{user['level']}

⭐ الخبرة:
{user['xp']}

👥 الدعوات:
{user['invites']}
"""

        )

    # =========================
    # INVITE
    # =========================

    elif data == "invite":

        invite_link = f"https://t.me/{BOT_USERNAME}?start={uid}"

        bot.send_message(

            call.message.chat.id,

            f"""
👥 رابط الدعوة:

{invite_link}

📊 الدعوات الناجحة:
{user['invites']}
"""

        )

    # =========================
    # COPY INVITE
    # =========================

    elif data == "copy_invite":

        invite_link = f"https://t.me/{BOT_USERNAME}?start={uid}"

        kb = telebot.types.InlineKeyboardMarkup()

        kb.add(

            telebot.types.InlineKeyboardButton(

                text="نسخ الرابط",

                copy_text=telebot.types.CopyTextButton(

                    text=invite_link

                ),

                style=DANGER

            )

        )

        bot.send_message(

            call.message.chat.id,

            f"""
👥 رابط الدعوة الخاص بك:

{invite_link}
""",

            reply_markup=kb

        )

    # =========================
    # LEVEL
    # =========================

    elif data == "level":

        need = user["level"] * 100

        bot.send_message(

            call.message.chat.id,

            f"""
🏆 مستواك الحالي

📈 المستوي:
{user['level']}

⭐ الخبرة:
{user['xp']} / {need}
"""

        )

    # =========================
    # STATS
    # =========================

    elif data == "stats":

        bot.send_message(

            call.message.chat.id,

            f"""
📊 الإحصائيات

👥 المستخدمين:
{len(db['users'])}

📦 المنتجات:
{len(db['products'])}

📂 القوائم:
{len(db['categories'])}

🛒 الطلبات:
{len(db['orders'])}
"""

        )

    # =========================
    # TASKS
    # =========================

    elif data == "tasks":

        bot.send_message(

            call.message.chat.id,

            """
📋 المهام قريباً
"""

        )

    # =========================
    # COUPON
    # =========================

    elif data == "coupon":

        bot.send_message(

            call.message.chat.id,

            f"""
🎟 الخصم الحالي

{settings['discount']}%
"""

        )

    # =========================
    # DEVELOPER
    # =========================

    elif data == "developer":

        kb = telebot.types.InlineKeyboardMarkup()

        kb.add(

            telebot.types.InlineKeyboardButton(

                text="@Asernoby23",

                url="https://t.me/Asernoby23",

                style=DANGER

            )

        )

        bot.send_message(

            call.message.chat.id,

            """
👨‍💻 المطور الرسمي
""",

            reply_markup=kb

        )

    # =========================
    # ADMIN
    # =========================

    elif data == "admin":

        open_admin_panel(
            bot,
            call,
            btn
        )

    # =========================
    # SHOP
    # =========================

    shop_callbacks(
        bot,
        call,
        db,
        save_db,
        btn,
        ADMIN_ID
    )

    # =========================
    # ADMIN CALLBACKS
    # =========================

    admin_callbacks(
        bot,
        call,
        db,
        save_db,
        btn
    )

# =========================
# MESSAGE HANDLER
# =========================

@bot.message_handler(
    func=lambda m:True,
    content_types=[
        "text",
        "photo",
        "document",
        "video",
        "audio",
        "voice"
    ]
)
def messages(msg):

    db = load_db()

    uid = msg.from_user.id

    create_user(db,uid)

    # =========================
    # TRANSFER
    # =========================

    if uid in transfer_steps:

        if not msg.text:

            return bot.reply_to(

                msg,

                "❌ أرسل التحويل كنص"

            )

        try:

            uid2,amount = msg.text.split("|")

            amount = int(amount)

            uid2 = str(uid2)

            if amount <= 0:

                return bot.reply_to(

                    msg,

                    "❌ رقم غير صالح"

                )

            if db["users"][str(uid)]["mc"] < amount:

                return bot.reply_to(

                    msg,

                    "❌ رصيدك لا يكفي"

                )

            create_user(db,uid2)

            db["users"][str(uid)]["mc"] -= amount

            db["users"][uid2]["mc"] += amount

            save_db(db)

            del transfer_steps[uid]

            bot.reply_to(

                msg,

                f"""
✅ تم التحويل بنجاح

💰 {amount} MineCoin
"""

            )

            bot.send_message(

                uid2,

                f"""
🎁 وصلك تحويل جديد

💰 {amount} MineCoin
"""

            )

        except:

            bot.reply_to(

                msg,

                """
❌ الصيغة خطأ

ايدي|عدد
"""

            )

        return

    # =========================
    # ADMIN SYSTEM
    # =========================

    admin_messages(
        bot,
        msg,
        db,
        save_db
    )

# =========================
# RUN
# =========================

print("BOT STARTED")

bot.infinity_polling()