import os, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

ROADMAP_LINKS = {
    "cse_rm_ai": "رابط مسار AI & Machine learning:\n🔗https://qr1.me-qr.com/mobile/pdf/4a687b37-8557-4f38-92ac-5f621fedd2c1",
    "cse_rm_ds": "رابط مسار علم البيانات (Data Science):\n🔗https://qr1.me-qr.com/mobile/pdf/63e394f8-a86b-4e3e-9455-f2151b4f12b5",
    "cse_rm_robotics": "رابط مسار الروبوتات:\n🔗https://qr1.me-qr.com/mobile/pdf/d1770eda-eaec-47c7-aefe-d6b04597d1d9",
    "cse_rm_cyber": "رابط مسار الأمن السيبراني:\n🔗https://qr1.me-qr.com/mobile/pdf/f4e9fa7c-f7ec-49a4-9243-f47fe7c6fdfd",
    "cse_rm_fullstack": "رابط مسار الفل ستاك(full stack developer):\n🔗https://qr1.me-qr.com/mobile/pdf/a51e8960-56fa-4612-a106-ad53ee7fa2a3",
    "cse_rm_frontend": "رابط مسار الفرونت إند(frontend developer):\n🔗https://qr1.me-qr.com/mobile/pdf/cd5c2ece-0e69-4ddd-b084-a49708d41b42",
    "cse_rm_backend": "رابط مسار الباك إند (backend developer):\n🔗https://qr1.me-qr.com/mobile/pdf/5f99a65a-fc13-4819-bd44-9168c187134b",
    "cse_rm_mobile": "رابط مسار الأندرويد:\n🔗https://qr1.me-qr.com/mobile/pdf/994f5141-2fd1-462a-8892-10d0982ed45b\n\nرابط مسار IOS:\n🔗https://qr1.me-qr.com/mobile/pdf/a53e5055-04e7-401d-ae16-5ee0809503d2",
    "cse_rm_uiux": "رابط مسار تصميم واجهة المستخدم (UI/UX designer):\n🔗https://qr1.me-qr.com/mobile/pdf/3698c9fa-53a8-4284-9ce7-d2052847bc8a",
    "cse_rm_qa": "رابط مسار ضمان الجودة (QA Engineer):\n🔗https://qr1.me-qr.com/mobile/pdf/79c31563-de01-4d08-a618-92cad8d4d535",
    "cse_rm_lowlevel": "رابط مسار اللغات منخفضة المستوى (LL Programming):\n🔗https://qr1.me-qr.com/mobile/pdf/42137ab5-0755-4824-9f23-707f8f2e3df0",
    "cse_rm_game": "رابط مسار تطوير الألعاب (Game Developer):\n🔗https://qr1.me-qr.com/mobile/pdf/3f97d69d-378b-44a2-b8b5-662263da891c",
}

# =========================
# Helpers
# =========================

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💻 هندسة الحاسوب", callback_data="cse"), InlineKeyboardButton("📡 هندسة الاتصالات", callback_data="te")],
        [InlineKeyboardButton("⚙️ هندسة الميكانيك", callback_data="me"), InlineKeyboardButton("⚙️ هندسة الميكاترونيكس", callback_data="me")],
        [InlineKeyboardButton("⚡ الهندسة الكهربائية والأتمتة الصناعية", callback_data="ee")],
        [InlineKeyboardButton("🏗 هندسة البناء", callback_data="ce"), InlineKeyboardButton("🏗 الهندسة المدنية", callback_data="ce")],
        [InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq")]
    ])


def specialization_menu(spec_code: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 المواد", callback_data=f"{spec_code}_subjects"), InlineKeyboardButton("Roadmaps", callback_data=f"{spec_code}_roadmaps")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ])



def subjects_menu(spec_code: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(" إجباري جامعة", callback_data=f"{spec_code}_um"), InlineKeyboardButton(" إجباري كلية", callback_data=f"{spec_code}_cm"), InlineKeyboardButton(" إجباري تخصص", callback_data=f"{spec_code}_dm")],
        [InlineKeyboardButton(" اختياري جامعة", callback_data=f"{spec_code}_uo"), InlineKeyboardButton(" اختياري تخصص", callback_data=f"{spec_code}_do")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=spec_code), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
    ])


def subject_content_menu(back_callback: str, with_reports=False):
    keyboard = [
        [InlineKeyboardButton("📄 تلاخيص", callback_data="link"), InlineKeyboardButton("🎥 شروحات", callback_data="link"), InlineKeyboardButton("📘 الكتاب", callback_data="link")],
        [InlineKeyboardButton("📝 امتحانات", callback_data="link"), InlineKeyboardButton("📂 واجبات", callback_data="link")]
    ]
    if with_reports:
        keyboard.append([InlineKeyboardButton("📑 تقارير", callback_data="link")])

    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)], InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main"))
    return InlineKeyboardMarkup(keyboard)


# =========================
# Commands
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        "👋 أهلاً بك في بوت الهندسة الجامعية\n\n"
        "📌 **طريقة استخدام البوت:**\n"
        "• البوت يعمل بالكامل عبر الأزرار.\n"
        "• اختر تخصصك من القائمة الرئيسية.\n"
        "• ادخل إلى قسم المواد ثم اختر نوع المادة.\n"
        "• داخل كل مادة ستجد التلاخيص، الشروحات، الكتب، الامتحانات وغيرها.\n"
        "• يمكنك دائمًا الرجوع باستخدام زر (رجوع).\n\n"
        "💡 لأي ملاحظات أو اقتراحات استخدم الأمر:\n"
        "/note\n\n"
        "👇 اختر من القائمة:"
    )

    await update.message.reply_text(
        intro_text,
        reply_markup=main_menu_keyboard()
    )


async def inst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 هذا البوت تعليمي يعتمد على القوائم.\n"
        "تنقّل بين التخصصات والمواد باستخدام الأزرار فقط."
    )


async def bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 البوتات المرتبطة:\n"
        "@tamfk2006\n"
        "@Tak6Bot\n"
        "@IVR_Library_bot"
    )


# =========================
# Callback Buttons
# =========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ---- Main specializations ----
    if data in ["cse", "me", "ee", "te", "ce"]:
        titles = {
            "cse": "💻 هندسة الحاسوب",
            "me": "⚙️ هندسة الميكانيك والميكاترونيكس",
            "ee": "⚡ الهندسة الكهربائية والأتمتة الصناعية",
            "te": "📡 هندسة الاتصالات",
            "ce": "🏗 هندسة البناء والهندسة المدنية"
        }

        await query.edit_message_text(
            text=titles[data],
            reply_markup=specialization_menu(data)
        )


    # ---- Subjects ----
    elif data.endswith("_subjects"):
        spec = data.replace("_subjects", "")
        await query.edit_message_text(
            text="      📘 اخـــــــتــــــر نـــــــوع الــــــمـــــواد:      ",
            reply_markup=subjects_menu(spec)
        )

    # ---- Subject lists (example implementation) ----
    elif data.endswith(("_um", "_cm", "_dm", "_do", "_uo")):
        await query.edit_message_text(
            text="📚 اختر مادة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("مادة 1", callback_data=f"{data}_s1")],
                [InlineKeyboardButton("مادة 2", callback_data=f"{data}_s2")],
                [InlineKeyboardButton("مادة 3", callback_data=f"{data}_s3")],
                [InlineKeyboardButton("مادة 4", callback_data=f"{data}_s4")],
                [InlineKeyboardButton("🔙 رجوع", callback_data=data.split("_")[0] + "_subjects"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    # ---- Inside subject ----
    elif "_s" in data:
        with_reports = data.startswith("cse_cm")  # مثال: مواد كلية فيها تقارير
        await query.edit_message_text(
            text="📖 محتوى المادة:",
            reply_markup=subject_content_menu(
                back_callback=data.rsplit("_", 1)[0],
                with_reports=with_reports
            )
        )

    # ---- Roadmaps ----
    elif data == "cse_roadmaps":
        keyboard = [
            [InlineKeyboardButton("🤖 AI & Machine Learning", callback_data="cse_rm_ai")],
            [InlineKeyboardButton("📊 Data Science", callback_data="cse_rm_ds"), InlineKeyboardButton("🤖 Robotics", callback_data="cse_rm_robotics")],
            [InlineKeyboardButton("🔐 Cybersecurity", callback_data="cse_rm_cyber"), InlineKeyboardButton("🌐 Full Stack Developer", callback_data="cse_rm_fullstack")],
            [InlineKeyboardButton("🎨 Frontend", callback_data="cse_rm_frontend"), InlineKeyboardButton("🧠 Backend", callback_data="cse_rm_backend")],
            [InlineKeyboardButton("📱 Mobile Application", callback_data="cse_rm_mobile"), InlineKeyboardButton("🖌 UI / UX", callback_data="cse_rm_uiux")],
            [InlineKeyboardButton("🧪 QA", callback_data="cse_rm_qa"), InlineKeyboardButton("🎮 Game Developer", callback_data="cse_rm_game")],
            [InlineKeyboardButton("⚙ Low Level Programming", callback_data="cse_rm_lowlevel")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="cse"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
        ]

        await query.edit_message_text(
            text="🗺 Roadmaps – هندسة الحاسوب",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data in ROADMAP_LINKS:
        await query.message.reply_text(
            f"{ROADMAP_LINKS[data]}"
    )

        await query.message.reply_text(
            "🗺 Roadmaps – هندسة الحاسوب",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="cse_roadmaps"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    # ---- FAQ ----
    elif data == "faq":
        keyboard = [
            [InlineKeyboardButton("🏫 عن الجامعة", callback_data="faq_university"), InlineKeyboardButton("🎓 عن المنح", callback_data="faq_scholarships"), InlineKeyboardButton("👨‍🏫 عن المدرسين", callback_data="faq_teachers")],
            [InlineKeyboardButton("📚 عن الدراسة وطرقها", callback_data="faq_study"), InlineKeyboardButton("🐣 أسئلة سنافر", callback_data="faq_freshmen"), InlineKeyboardButton("💡 نصائح", callback_data="faq_tips")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]

        await query.edit_message_text(
            text="❓ الأسئلة الشائعة:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "faq_university":
        await query.edit_message_text(
            text="🏫 عن الجامعة:\n\n"
                 "س: هل الجامعة معترف بها؟\n"
                 "ج: نعم، الجامعة معترف بها رسميًا.\n\n"
                 "س: أين تقع الجامعة؟\n"
                 "ج: يتم تحديد الموقع حسب الكلية.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_scholarships":
        await query.edit_message_text(
            text="🎓 عن المنح:\n\n"
                 "س: هل توجد منح؟\n"
                 "ج: نعم، توجد منح تفوق ومنح دعم.\n\n"
                 "س: كيف أقدم على منحة؟\n"
                 "ج: عبر شؤون الطلاب.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_study":
        await query.edit_message_text(
            text="📚 عن الدراسة وطرقها:\n\n"
                 "س: هل الدراسة صعبة؟\n"
                 "ج: تحتاج التزام وتنظيم وقت.\n\n"
                 "س: هل المحاضرات مسجلة؟\n"
                 "ج: يعتمد على المادة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_teachers":
        await query.edit_message_text(
            text="👨‍🏫 عن المدرسين:\n\n"
                 "س: هل المدرسون متعاونون؟\n"
                 "ج: أغلبهم متعاونون داخل المحاضرات.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_freshmen":
        await query.edit_message_text(
            text="🐣 أسئلة سنافر:\n\n"
                 "س: ماذا أدرس أولًا؟\n"
                 "ج: ركز على الأساسيات.\n\n"
                 "س: كيف أنظم وقتي؟\n"
                 "ج: جدول أسبوعي بسيط.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_tips":
        await query.edit_message_text(
            text="💡 نصائح:\n\n"
                 "• لا تؤجل الدراسة\n"
                 "• تابع التلاخيص\n"
                 "• اسأل ولا تتردد",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    # ---- Back to main ----
    elif data == "back_main":
        await query.edit_message_text(
            text="👇 اختر من القائمة:",
            reply_markup=main_menu_keyboard()
        )
    # ---- Remove the sent note ----
    elif data == "delete_note":
        msg_id = context.user_data.get("last_note_msg_id")
        note_time = context.user_data.get("note_time")

        if not msg_id or not note_time:
            await query.answer("❌ لا توجد ملاحظة للحذف", show_alert=True)
            return

        if time.time() - note_time > 5:
            await query.answer("⏱ انتهت مهلة الحذف", show_alert=True)
            await query.message.edit_text("❌ انتهت مهلة حذف الملاحظة.")
            return

        await context.bot.delete_message(
            chat_id=TARGET_CHAT_ID,
            message_id=msg_id
        )

        await query.message.edit_text("🗑 تم حذف الملاحظة بنجاح.")
# =========================
# Notes forwarding
# =========================

TARGET_CHAT_ID = -1002905917338

async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_note"] = True
    await update.message.reply_text("✍️ أرسل الملاحظة الآن:")


async def handle_note_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_note"):
        user = update.effective_user
        note_text = update.message.text
        username_text = f"@{user.username}" if user.username else "—"
        full_message = (
            "📩 ملاحظة جديدة\n\n"
            f"📝 النص:\n{note_text}\n\n"
            "──────────────\n"
            f"👤 الاسم: {user.full_name}\n"
            f"🆔 Telegram ID: {user.id}\n"
             f"🔗 Username: {username_text}"
        )

        sent_msg = await context.bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=full_message
        )

        # حفظ بيانات الحذف
        context.user_data["last_note_msg_id"] = sent_msg.message_id
        context.user_data["note_time"] = time.time()

        await update.message.reply_text(
    "✅ تم إرسال الملاحظة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗑 حذف الملاحظة", callback_data="delete_note")]
            ])
)
        context.user_data["waiting_for_note"] = False


# =========================
# Main
# =========================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("inst", inst))
    app.add_handler(CommandHandler("bots", bots))
    app.add_handler(CommandHandler("note", note_command))

    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note_text))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
