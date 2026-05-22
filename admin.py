# =========================
# ADMIN.PY
# =========================

import telebot

steps = {}

# =========================
# OPEN ADMIN PANEL
# =========================

def open_admin_panel(bot,call,btn):

    kb = telebot.types.InlineKeyboardMarkup(
        row_width=1
    )

    kb.add(

        btn(
            "إضافة قائمة",
            "add_category",
            "danger"
        ),

        btn(
            "حذف قائمة",
            "delete_category",
            "danger"
        )

    )
    kb.add(

    btn(
        "📋 عرض القوائم",
        "show_categories",
        "danger"
    )
)

    kb.add(

        btn(
            "إضافة منتج",
            "add_product",
            "danger"
        ),

        btn(
            "حذف منتج",
            "delete_product",
            "danger"
        )

    )

    kb.add(

        btn(
            "إضافة MineCoin",
            "give_mc",
            "danger"
        ),

        btn(
            "سحب MineCoin",
            "remove_mc",
            "danger"
        )

    )

    
    kb.add(

        btn(
            "تعديل اليومي",
            "edit_daily",
            "danger"
        )

    )

    kb.add(

        btn(
            "تعديل الدعوات",
            "edit_invite",
            "danger"
        )

    )

    kb.add(

        btn(
            "تعديل الخصم",
            "edit_discount",
            "danger"
        ),

        btn(
            "تعديل الضريبة",
            "edit_tax",
            "danger"
        )

    )

    kb.add(

        btn(
            "إحصائيات البوت",
            "admin_stats",
            "danger"
        )

    )

    bot.send_message(

        call.message.chat.id,

        """
⚙️ لوحة تحكم الأدمن
عدل الازرار التي تريدها
""",

        reply_markup=kb

    )

# =========================
# CALLBACKS
# =========================

def admin_callbacks(bot,call,db,save_db,btn):

    uid = call.from_user.id

    data = call.data

    # =========================
    # ADD CATEGORY
    # =========================

    if data == "add_category":

        steps[uid] = {

            "type":"add_category"

        }

        return bot.send_message(

            call.message.chat.id,

            """
📂 أرسل اسم القائمة الجديدة
"""

        )

    # =========================
    # DELETE CATEGORY
    # =========================

    elif data == "delete_category":

        steps[uid] = {

            "type":"delete_category"

        }

        return bot.send_message(

            call.message.chat.id,

            """
🗑 أرسل اسم القائمة للحذف
"""

        )

    elif data == "show_categories":

         text = "📂 القوائم الموجودة:\n\n"

         if not db["categories"]:

               text += "❌ مفيش قوائم"

         else:

               for cid, cat in db["categories"].items():

                    text += f"""
📁 الاسم: {cat['name']}
🆔 ID: {cid}
━━━━━━━━━━━━━━
"""

         return bot.send_message(

               call.message.chat.id,

               text

          )

    # =========================
    # ADD PRODUCT
    # =========================

    elif data == "add_product":

        steps[uid] = {

            "type":"add_product",

            "step":"name"

        }

        return bot.send_message(

            call.message.chat.id,

            """
📦 أرسل اسم المنتج
"""

        )

    # =========================
    # DELETE PRODUCT
    # =========================

    elif data == "delete_product":

        steps[uid] = {

            "type":"delete_product"

        }

        return bot.send_message(

            call.message.chat.id,

            """
🗑 أرسل اسم المنتج للحذف
"""

        )

    # =========================
    # GIVE MC
    # =========================

    elif data == "give_mc":

        steps[uid] = {

            "type":"give_mc"

        }

        return bot.send_message(

            call.message.chat.id,

            """
💰 أرسل:

ايدي|عدد
"""
    )
#--------------------------------
#--------------------------------

        

    # =========================
    # REMOVE MC
    # =========================

    elif data == "remove_mc":

        steps[uid] = {

            "type":"remove_mc"

        }

        return bot.send_message(

            call.message.chat.id,

            """
💸 أرسل:

ايدي|عدد
"""

        )

    # =========================
    # EDIT MINE
    # =========================

    elif data == "edit_mine":

          try:

               mine_min, mine_max = msg.text.split("|")

               mine_min = int(mine_min)
               mine_max = int(mine_max)

               db["settings"]["mine_min"] = mine_min
               db["settings"]["mine_max"] = mine_max

               save_db(db)

               del steps[uid]

               return bot.reply_to(

                    msg,

                    f"""
✅ تم تعديل التعدين

⛏ الأقل:
{mine_min}

⛏ الأعلى:
{mine_max}
"""

               )

          except:

               return bot.reply_to(

                    msg,

                    """
❌ الصيغة خطأ

اكتب:
اقل|اعلي

مثال:
5|20
"""

               )

    # =========================
    # EDIT COOLDOWN
    # =========================

    elif data == "edit_cooldown":

          try:

               cooldown = int(msg.text)

               db["settings"]["mine_cooldown"] = cooldown

               save_db(db)

               del steps[uid]

               return bot.reply_to(

                    msg,

                    f"""
✅ تم تعديل مدة التعدين

⏳ المدة:
{cooldown} ثانية
"""

               )

          except:

               return bot.reply_to(

                    msg,

                    "❌ ارسل رقم صحيح"

               )

    # =========================
    # EDIT DAILY
    # =========================

    elif data == "edit_daily":

        steps[uid] = {

            "type":"edit_daily"

        }

        return bot.send_message(

            call.message.chat.id,

            """
🎁 أرسل قيمة اليومي
"""

        )

    # =========================
    # EDIT INVITE
    # =========================

    elif data == "edit_invite":

        steps[uid] = {

            "type":"edit_invite"

        }

        return bot.send_message(

            call.message.chat.id,

            """
👥 أرسل قيمة الدعوات
"""

        )

    # =========================
    # EDIT DISCOUNT
    # =========================

    elif data == "edit_discount":

        steps[uid] = {

            "type":"edit_discount"

        }

        return bot.send_message(

            call.message.chat.id,

            """
🎟 أرسل نسبة الخصم
"""

        )

    # =========================
    # EDIT TAX
    # =========================

    elif data == "edit_tax":

        steps[uid] = {

            "type":"edit_tax"

        }

        return bot.send_message(

            call.message.chat.id,

            """
💳 أرسل نسبة الضريبة
"""

        )

    # =========================
    # STATS
    # =========================

    elif data == "admin_stats":

        return bot.send_message(

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
# ADMIN MESSAGES
# =========================

def admin_messages(bot,msg,db,save_db):

    uid = msg.from_user.id

    if uid not in steps:
        return

    data = steps[uid]

    # =========================
    # ADD CATEGORY
    # =========================

    if data["type"] == "add_category":

        cid = str(
            len(db["categories"]) + 1
        )

        db["categories"][cid] = {

            "name":msg.text

        }

        save_db(db)

        del steps[uid]

        return bot.reply_to(

            msg,

            f"""
✅ تم إضافة القائمة

📂 الاسم:
{msg.text}

🆔 ID:
{cid}
"""

        )

    # =========================
    # DELETE CATEGORY
    # =========================

    elif data["type"] == "delete_category":

        found = None

        for cid,cat in db["categories"].items():

            if cat["name"] == msg.text:

                found = cid

        if found:

            del db["categories"][found]

            save_db(db)

            del steps[uid]

            return bot.reply_to(

                msg,

                "✅ تم حذف القائمة"

            )

        return bot.reply_to(

            msg,

            "❌ القائمة غير موجودة"

        )

    # =========================
    # DELETE PRODUCT
    # =========================

    elif data["type"] == "delete_product":

        found = None

        for pid,p in db["products"].items():

            if p["name"] == msg.text:

                found = pid

        if found:

            del db["products"][found]

            save_db(db)

            del steps[uid]

            return bot.reply_to(

                msg,

                "✅ تم حذف المنتج"

            )

        return bot.reply_to(

            msg,

            "❌ المنتج غير موجود"

        )

    # =========================
    # ADD PRODUCT
    # =========================

    elif data["type"] == "add_product":

        # =========================
        # NAME
        # =========================

        if data["step"] == "name":

            data["name"] = msg.text

            data["step"] = "price"

            return bot.reply_to(

                msg,

                "💰 أرسل السعر"

            )

        # =========================
        # PRICE
        # =========================

        elif data["step"] == "price":

            data["price"] = int(msg.text)

            data["step"] = "desc"

            return bot.reply_to(

                msg,

                "📝 أرسل الوصف"

            )

        # =========================
        # DESC
        # =========================

        elif data["step"] == "desc":

            data["desc"] = msg.text

            data["step"] = "content"

            return bot.reply_to(

                msg,

                """
📥 أرسل محتوى المنتج

يمكن إرسال:
• نص
• صورة
• ملف
• فيديو
• صوت
• رابط
"""

            )

        # =========================
        # CONTENT
        # =========================

        elif data["step"] == "content":

            # =========================
            # TEXT
            # =========================

            if msg.text:

                data["content_type"] = "text"

                data["content"] = msg.text

            # =========================
            # PHOTO
            # =========================

            elif msg.photo:

                data["content_type"] = "photo"

                data["content"] = msg.photo[-1].file_id

            # =========================
            # DOCUMENT
            # =========================

            elif msg.document:

                data["content_type"] = "document"

                data["content"] = msg.document.file_id

            # =========================
            # VIDEO
            # =========================

            elif msg.video:

                data["content_type"] = "video"

                data["content"] = msg.video.file_id

            # =========================
            # AUDIO
            # =========================

            elif msg.audio:

                data["content_type"] = "audio"

                data["content"] = msg.audio.file_id

            # =========================
            # VOICE
            # =========================

            elif msg.voice:

                data["content_type"] = "voice"

                data["content"] = msg.voice.file_id

            else:

                return bot.reply_to(

                    msg,

                    "❌ نوع غير مدعوم"

                )

            data["step"] = "category"

            return bot.reply_to(

                msg,

                """
📂 أرسل ID القائمة
"""

            )

        # =========================
        # CATEGORY
        # =========================

        elif data["step"] == "category":

            pid = str(
                len(db["products"]) + 1
            )

            db["products"][pid] = {

                "name":data["name"],

                "price":data["price"],

                "desc":data["desc"],

                "content":data["content"],

                "content_type":data["content_type"],

                "category":msg.text,

                "stock":"unlimited"

            }

            save_db(db)

            del steps[uid]

            return bot.reply_to(

                msg,

                f"""
✅ تم إضافة المنتج

📦 الاسم:
{data['name']}

🆔 ID:
{pid}
"""

            )

    # =========================
    # GIVE MC
    # =========================

    elif data["type"] == "give_mc":

        uid2,amount = msg.text.split("|")

        amount = int(amount)

        if uid2 not in db["users"]:

            db["users"][uid2] = {

                "mc":0,

                "mine":0,

                "daily":0,

                "invites":0,

                "joined":False,

                "level":1,

                "xp":0

            }

        db["users"][uid2]["mc"] += amount

        save_db(db)

        del steps[uid]

        return bot.reply_to(

            msg,

            "✅ تم إضافة MineCoin"

        )

    # =========================
    # REMOVE MC
    # =========================

    elif data["type"] == "remove_mc":

        uid2,amount = msg.text.split("|")

        amount = int(amount)

        if uid2 in db["users"]:

            db["users"][uid2]["mc"] -= amount

        save_db(db)

        del steps[uid]

        return bot.reply_to(

            msg,

            "✅ تم سحب MineCoin"

        )

    # =========================
    # EDIT MINE
    # =========================

    elif data["type"] == "edit_mine":

         try:

              mine_min, mine_max = msg.text.split("|")

              mine_min = int(mine_min)
              mine_max = int(mine_max)

              db["settings"]["mine_min"] = mine_min
              db["settings"]["mine_max"] = mine_max

              save_db(db)

              del steps[uid]

              return bot.reply_to(

                   msg,

                   f"""
✅ تم تعديل التعدين

⛏ الأقل:
{mine_min}

⛏ الأعلى:
{mine_max}
"""

              )

         except:

              return bot.reply_to(

                   msg,

                   """
❌ الصيغة خطأ

اقل|اعلي

مثال:
5|20
"""

              )

    # =========================
    # EDIT COOLDOWN
    # =========================

    elif data["type"] == "edit_cooldown":

         try:

              cooldown = int(msg.text)

              db["settings"]["mine_cooldown"] = cooldown

              save_db(db)

              del steps[uid]

              return bot.reply_to(

                   msg,

                   f"""
✅ تم تعديل مدة التعدين

⏳ المدة:
{cooldown} ثانية
"""

              )

         except:

              return bot.reply_to(

                   msg,

                   "❌ ارسل رقم صحيح"

              )

    # =========================
    # EDIT DAILY
    # =========================

    elif data["type"] == "edit_daily":

        db["settings"]["daily_reward"] = int(msg.text)

        save_db(db)

        del steps[uid]

        return bot.reply_to(

            msg,

            "✅ تم تعديل اليومي"

        )

    # =========================
    # EDIT INVITE
    # =========================

    elif data["type"] == "edit_invite":

        db["settings"]["invite_reward"] = int(msg.text)

        save_db(db)

        del steps[uid]

        return bot.reply_to(

            msg,

            "✅ تم تعديل الدعوات"

        )

    # =========================
    # EDIT DISCOUNT
    # =========================

    elif data["type"] == "edit_discount":

        db["settings"]["discount"] = int(msg.text)

        save_db(db)

        del steps[uid]

        return bot.reply_to(

            msg,

            "✅ تم تعديل الخصم"

        )

    # =========================
    # EDIT TAX
    # =========================

    elif data["type"] == "edit_tax":

        db["settings"]["tax"] = int(msg.text)

        save_db(db)

        del steps[uid]

        return bot.reply_to(

            msg,

            "✅ تم تعديل الضريبة"

        )