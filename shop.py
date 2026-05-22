# =========================
# SHOP.PY
# =========================

import telebot
import time

# =========================
# SHOP CALLBACKS
# =========================

def shop_callbacks(
    bot,
    call,
    db,
    save_db,
    btn,
    ADMIN_ID
):

    data = call.data

    uid = str(call.from_user.id)

    user = db["users"][uid]

    settings = db["settings"]

    # =========================
    # OPEN CATEGORIES
    # =========================

    if data == "categories":

        kb = telebot.types.InlineKeyboardMarkup(
            row_width=1
        )

        if not db["categories"]:

            return bot.send_message(

                call.message.chat.id,

                """
❌ لا توجد قوائم حالياً
"""

            )

        for cid,cat in db["categories"].items():

            kb.add(

                btn(

                    f"{cat['name']}",

                    f"category_{cid}",

                    "success"

                )

            )

        return bot.send_message(

            call.message.chat.id,

            """
📂 القوائم المتاحة   

يمكنك شراء اي منتج تريده ومعرفة معلوماته ℹ️

                        
""",

            reply_markup=kb

        )

    # =========================
    # OPEN CATEGORY
    # =========================

    elif data.startswith("category_"):

        cid = data.split("_")[1]

        kb = telebot.types.InlineKeyboardMarkup(
            row_width=1
        )

        found = False

        for pid,p in db["products"].items():

            if p["category"] == cid:

                found = True

                kb.add(

                    btn(

                        p["name"],

                        f"product_{pid}",

                        "primary"

                    )

                )

        if not found:

            return bot.send_message(

                call.message.chat.id,

                """
❌ لا توجد منتجات داخل هذه القائمة
"""

            )

        return bot.send_message(

            call.message.chat.id,

            """
📦 منتجات القائمة     

اختر المنتج الي تريده😄         




             
""",

            reply_markup=kb

        )

    # =========================
    # PRODUCT PAGE
    # =========================

    elif data.startswith("product_"):

        pid = data.split("_")[1]

        if pid not in db["products"]:
            return

        p = db["products"][pid]

        price = p["price"]

        # =========================
        # DISCOUNT
        # =========================

        discount = settings["discount"]

        if discount > 0:

            price = int(

                price - (
                    price * discount / 100
                )

            )

        # =========================
        # TAX
        # =========================

        tax = settings["tax"]

        if tax > 0:

            price = int(

                price + (
                    price * tax / 100
                )

            )

        stock = p.get(
            "stock",
            "unlimited"
        )

        if stock == "unlimited":

            stock_text = "♾ غير محدود"

        else:

            stock_text = str(stock)

        text = f"""
📦 المنتج:
{p['name']}

📝 الوصف:
{p['desc']}

💰 السعر النهائي:
{price} {settings['currency_name']}

🎟 الخصم:
{discount}%

💳 الضريبة:
{tax}%

📊 المخزون:
{stock_text}
"""

        kb = telebot.types.InlineKeyboardMarkup()

        kb.add(

            btn(

                "شراء المنتج",

                f"buy_{pid}",

                "success"

            )

        )

        return bot.send_message(

            call.message.chat.id,

            text,

            reply_markup=kb

        )

    # =========================
    # BUY PRODUCT
    # =========================

    elif data.startswith("buy_"):

        pid = data.split("_")[1]

        if pid not in db["products"]:
            return

        p = db["products"][pid]

        price = p["price"]

        # =========================
        # DISCOUNT
        # =========================

        discount = settings["discount"]

        if discount > 0:

            price = int(

                price - (
                    price * discount / 100
                )

            )

        # =========================
        # TAX
        # =========================

        tax = settings["tax"]

        if tax > 0:

            price = int(

                price + (
                    price * tax / 100
                )

            )

        # =========================
        # CHECK MONEY
        # =========================

        if user["mc"] < price:

            return bot.send_message(

                call.message.chat.id,

                """
❌ رصيدك لا يكفي لشراء المنتج
"""

            )

        # =========================
        # STOCK CHECK
        # =========================

        stock = p.get(
            "stock",
            "unlimited"
        )

        if stock != "unlimited":

            if int(stock) <= 0:

                return bot.send_message(

                    call.message.chat.id,

                    """
❌ المنتج نفذ من المخزون
"""

                )

            p["stock"] = int(stock) - 1

        # =========================
        # REMOVE MONEY
        # =========================

        user["mc"] -= price

        # =========================
        # SAVE ORDER
        # =========================

        db["orders"].append({

            "user":uid,

            "product":p["name"],

            "price":price,

            "time":int(time.time())

        })

        save_db(db)

        # =========================
        # SUCCESS
        # =========================

        bot.send_message(

            call.message.chat.id,

            f"""
✅ تم شراء المنتج بنجاح

📦 المنتج:
{p['name']}

💰 السعر:
{price} {settings['currency_name']}
"""

        )

        # =========================
        # SEND PRODUCT
        # =========================

        ctype = p.get(
            "content_type",
            "text"
        )

        content = p["content"]

        # =========================
        # TEXT
        # =========================

        if ctype == "text":

            bot.send_message(

                call.message.chat.id,

                f"""
📥 المنتج:

{content}
"""

            )

        # =========================
        # PHOTO
        # =========================

        elif ctype == "photo":

            bot.send_photo(

                call.message.chat.id,

                content,

                caption=f"""
📦 {p['name']}
"""

            )

        # =========================
        # DOCUMENT
        # =========================

        elif ctype == "document":

            bot.send_document(

                call.message.chat.id,

                content,

                caption=f"""
📦 {p['name']}
"""

            )

        # =========================
        # VIDEO
        # =========================

        elif ctype == "video":

            bot.send_video(

                call.message.chat.id,

                content,

                caption=f"""
📦 {p['name']}
"""

            )

        # =========================
        # AUDIO
        # =========================

        elif ctype == "audio":

            bot.send_audio(

                call.message.chat.id,

                content,

                caption=f"""
📦 {p['name']}
"""

            )

        # =========================
        # VOICE
        # =========================

        elif ctype == "voice":

            bot.send_voice(

                call.message.chat.id,

                content

            )

        # =========================
        # ADMIN NOTIFY
        # =========================

        bot.send_message(

            ADMIN_ID,

            f"""
🛒 عملية شراء جديدة

👤 المستخدم:
{uid}

📦 المنتج:
{p['name']}

💰 السعر:
{price}
"""

        )

    # =========================
    # ORDERS
    # =========================

    elif data == "orders":

        text = """
🛒 طلباتك

"""

        found = False

        for order in db["orders"]:

            if str(order["user"]) == uid:

                found = True

                text += f"""
📦 {order['product']}
💰 {order['price']}

"""

        if not found:

            text += """
❌ لا توجد طلبات
"""

        return bot.send_message(

            call.message.chat.id,

            text

        )