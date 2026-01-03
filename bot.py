import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 هندسة أنظمة الحاسوب", callback_data="cse")],
        [InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq")],
        [InlineKeyboardButton("📚 هندسة الميكانيك", callback_data="me")], 
        [InlineKeyboardButton("📚 الهندسة الكهربائية", callback_data="ee")], 
        [InlineKeyboardButton("📚 هندسة الطاقة", callback_data="ene")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك 👋\nاختر ما تريد:",
        reply_markup=reply_markup
    )
async def inst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هذا البوت يعمل عن طريق الأزرار، اختر الخيار الذي تريده للوصول إلى المادة التي تحتاجها، البوت فيه أقسام للمواد وشروحاتها وملخصاتها وكتبها، وأيضاً فيه أقسام للأسئلة الشائعة والاستفسارات، لأي ملاحظات أو تعديلات يمكنكم إرسال /note ثم إرسال الملاحظة ")
async def bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بوت المساعد الذكي: @tamfk2006\nبوت الامتحانات: @Tak6Bot\بوت المكتبة: @IVR_Library_bot")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cse":
        keyboard = [
            [InlineKeyboardButton("📘 المواد", callback_data="subjects")],
            [InlineKeyboardButton("🗺 Roadmaps", callback_data="roadmaps")],
            [InlineKeyboardButton("رجوع ➔", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="هندسة أنظمة الحاسوب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "faq":
        keyboard = [
          [InlineKeyboardButton("رجوع ➔", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text=
            "❓ الأسئلة الشائعة:\n\n• كيف أجد مواد كل مساق؟\n→ من قسم المواد.\n\n• هل المحتوى يتحدث؟\n→ نعم، يتم تحديثه دوريًا.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "subjects":
        keyboard = [
            [InlineKeyboardButton("🧮 مواد السنة الأولى", callback_data="cse_year1")],
            [InlineKeyboardButton("💻 مواد السنة الثانية", callback_data="cse_year2")],
            [InlineKeyboardButton("⚙️ مواد السنة الثالثة", callback_data="cse_year3")],
            [InlineKeyboardButton("رجوع ➔", callback_data="back_cse")]
        ]
        await query.edit_message_text(
            text="📘 مواد هندسة أنظمة الحاسوب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "back_cse":
        keyboard = [
          [InlineKeyboardButton("📘 المواد", callback_data="subjects")],
          [InlineKeyboardButton("🗺 Roadmaps", callback_data="roadmaps")],
          [InlineKeyboardButton("رجوع ➔", callback_data="back_main")]
          
        ]
        await query.edit_message_text(
          text="هندسة أنظمة الحاسوب:",
          reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "back_main":
      keyboard = [
          [InlineKeyboardButton("📚 هندسة أنظمة الحاسوب", callback_data="cse")],
          [InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq")],
          [InlineKeyboardButton("📚 هندسة الميكانيك", callback_data="me")], 
          [InlineKeyboardButton("📚 الهندسة الكهربائية", callback_data="ee")], 
          [InlineKeyboardButton("📚 هندسة الطاقة", callback_data="ene")] 
      ]
      await query.edit_message_text(
        text="أهلاً بك 👋\nاختر ما تريد:",
        reply_markup=InlineKeyboardMarkup(keyboard)
      )
    elif query.data == "roadmaps":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "resonsOfIOSStrength.docx")

    # إرسال الملف كرسالة مستقلة
        await query.message.reply_document(
            document=open(file_path, "rb"),
            caption="🗺 Roadmap هندسة أنظمة الحاسوب"
    )

    # إرسال قائمة جديدة بدل تعديل القديمة
        keyboard = [
            [InlineKeyboardButton("📘 المواد", callback_data="subjects")],
            [InlineKeyboardButton("🗺 Roadmaps", callback_data="roadmaps")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]

        await query.message.reply_text(
            text="هندسة أنظمة الحاسوب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

      
        keyboard = [
            [InlineKeyboardButton("📘 المواد", callback_data="subjects")],
            [InlineKeyboardButton("🗺 Roadmaps", callback_data="roadmaps")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="هندسة أنظمة الحاسوب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_note"] = True
    await update.message.reply_text(
        "✍️ أرسل الآن النص الذي تريد توجيهه:"
    )

TARGET_CHAT_ID = -5156036324

async def handle_note_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_note"):
        await context.bot.forward_message(
        chat_id=TARGET_CHAT_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
)


        await update.message.reply_text("✅ تم إرسال الملاحظة بنجاح.")
        context.user_data["waiting_for_note"] = False


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("inst", inst))
    app.add_handler(CommandHandler("bots", bots))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(CommandHandler("note", note_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note_text))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
