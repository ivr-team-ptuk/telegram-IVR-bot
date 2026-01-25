import os, time, re, json
from datetime import datetime, timedelta
from pathlib import Path
from telegram.constants import ChatAction
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
TARGET_CHAT_ID = -1002905917338
TOPICS_FILE = "topics.json"
USERS_FILE = Path("users.json")

def load_users_stats():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"daily": {}, "monthly": {}, "yearly": {}}

def save_users_stats(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

USERS_STATS = load_users_stats()

def track_user(user_id: int):
    now = datetime.utcnow()

    day_key = now.strftime("%Y-%m-%d")
    month_key = now.strftime("%Y-%m")
    year_key = now.strftime("%Y")

    uid = str(user_id)

    # DAILY
    USERS_STATS["daily"].setdefault(day_key, [])
    if uid not in USERS_STATS["daily"][day_key]:
        USERS_STATS["daily"][day_key].append(uid)

    # MONTHLY
    USERS_STATS["monthly"].setdefault(month_key, [])
    if uid not in USERS_STATS["monthly"][month_key]:
        USERS_STATS["monthly"][month_key].append(uid)

    # YEARLY
    USERS_STATS["yearly"].setdefault(year_key, [])
    if uid not in USERS_STATS["yearly"][year_key]:
        USERS_STATS["yearly"][year_key].append(uid)

    save_users_stats(USERS_STATS)

def get_daily_stats():
    """الحصول على إحصائيات اليوم"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return len(USERS_STATS["daily"].get(today, []))

def get_monthly_stats():
    """الحصول على إحصائيات الشهر الحالي"""
    current_month = datetime.utcnow().strftime("%Y-%m")
    return len(USERS_STATS["monthly"].get(current_month, []))

def get_yearly_stats():
    """الحصول على إحصائيات السنة الحالية"""
    current_year = datetime.utcnow().strftime("%Y")
    return len(USERS_STATS["yearly"].get(current_year, []))

def get_total_users():
    """الحصول على إجمالي المستخدمين الفريدين"""
    all_users = set()
    for day_users in USERS_STATS["daily"].values():
        all_users.update(day_users)
    return len(all_users)

def get_today_date():
    """الحصول على تاريخ اليوم بتنسيق جميل"""
    return datetime.utcnow().strftime("%Y-%m-%d")

def get_current_month_name():
    """الحصول على اسم الشهر الحالي"""
    return datetime.utcnow().strftime("%B %Y")

def get_recent_days_stats(days=7):
    """الحصول على إحصائيات آخر 7 أيام"""
    recent_stats = {}
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        count = len(USERS_STATS["daily"].get(date, []))
        # تحويل التاريخ إلى تنسيق قصير (مثل: Jan 25)
        date_short = (datetime.utcnow() - timedelta(days=i)).strftime("%b %d")
        recent_stats[date_short] = count
    return recent_stats
    
async def users_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لوحة تحكم مبسطة تعرض الإحصائيات الأساسية"""
    query = update.callback_query
    await query.answer()

    # تحديث البيانات من الملف
    global USERS_STATS
    USERS_STATS = load_users_stats()

    # الحصول على التواريخ الحالية
    today = datetime.utcnow().strftime("%Y-%m-%d")
    current_month = datetime.utcnow().strftime("%Y-%m")
    current_year = datetime.utcnow().strftime("%Y")

    # حساب إحصائيات آخر يوم
    last_day_users = set()
    for i in range(1):
        date_key = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_users = USERS_STATS["daily"].get(date_key, [])
        last_day_users.update(day_users)
        last_day_users = set()
   
    # حساب إحصائيات آخر 7 أيام
    last_7_days_users = set()
    for i in range(7):
        date_key = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_users = USERS_STATS["daily"].get(date_key, [])
        last_7_days_users.update(day_users)

    # حساب إحصائيات آخر 30 يوم (شهر)
    last_30_days_users = set()
    for i in range(30):
        date_key = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_users = USERS_STATS["daily"].get(date_key, [])
        last_30_days_users.update(day_users)

    # إحصائيات السنة الحالية
    yearly_users = set()
    for month_key, users in USERS_STATS["monthly"].items():
        if month_key.startswith(current_year):
            yearly_users.update(users)

    # إجمالي المستخدمين
    all_users = set()
    for day_users in USERS_STATS["daily"].values():
        all_users.update(day_users)

    # إنشاء الرسالة
    message = f"""
📊 **لوحة التحكم - إحصائيات المستخدمين**

📈 **الإحصائيات الأساسية:**

🔹 **هذا اليوم:**
   • {len(last_day_users)} مستخدم

🔹 **آخر 7 أيام:**
   • {len(last_7_days_users)} مستخدم

🔹 **آخر 30 يوم (شهر):**
   • {len(last_30_days_users)} مستخدم

🔹 **السنة الحالية ({current_year}):**
   • {len(yearly_users)} مستخدم

🔹 **الإجمالي الكلي:**
   • {len(all_users)} مستخدم

⏰ آخر تحديث: {datetime.utcnow().strftime('%H:%M:%S')}
"""

    # إنشاء الأزرار
    keyboard = [
        [InlineKeyboardButton("🔙 رجوع", callback_data="dashboard")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
def load_topics():
    if not os.path.exists(TOPICS_FILE):
        return {}
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_topics(data):
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


topics = load_topics()

GRAD_PROJECTS = {

    #projects
        "te_grad_projects": "https://drive.google.com/drive/folders/1pW26jE-iZuMGFilp76ls9hOwin4f4V-P",
        "cse_grad_projects": "https://drive.google.com/drive/folders/1QCyDTwu8a2-YSQ8hOZBGTPgd_3LSYhhH",
        "mee_grad_projects": "https://drive.google.com/drive/folders/1lPYPF9EGaZk6Dd3k1wCir1MBFcvOpITT",
        "ce_grad_projects": "https://drive.google.com/drive/folders/1NTGTUa6gKje0IdQgj199bLTzCezEEnhV",
        "gee_grad_projects": "https://drive.google.com/drive/folders/1lXsh_RdiVR1mhw48uPn3R1K32USmGXS2",
        "me_grad_projects": "https://drive.google.com/drive/folders/1kg91mpS2gq2V1CvxKtAIjH86ovkmElQ2",
        "cve_grad_projects": "https://drive.google.com/drive/folders/1ZArELcmBMtltY0mOCQ92Fv7qq4bjqJ-m",
        "ee_grad_projects": "https://drive.google.com/drive/folders/11AxQeaKdYlmCmAQV08FfILaf5EjaudRo",

    #proposals
        "te_grad_proposals": "https://drive.google.com/drive/folders/1DpI50ghBKMXMTdNG1j4YazJfhgboVfrZ",
        "cse_grad_proposals": "https://drive.google.com/drive/folders/1OIyr8WlnxMXseMCpQ5sRVntukgNNKEl_?usp=drive_link",
        "mee_grad_proposals": "https://drive.google.com/drive/folders/1W-j-LnJDMDX5VD6IFtJ-s0sPBCtnaNSe?usp=sharing",
        "ce_grad_proposals": "https://drive.google.com/drive/folders/1vTsZt4ggme5-EBhPgz8ch4GUqoxV9FXo?usp=sharing",
        "gee_grad_proposals": "https://drive.google.com/drive/folders/1Qyw-UnvltPp90vMJI2c1SLE_Q3duzxQk?usp=sharing",
        "me_grad_proposals": "https://drive.google.com/drive/folders/1mCRkDn2-Cne26Acr2hyN4D1hTPtMSrg3?usp=sharing",
        "cve_grad_proposals": "https://drive.google.com/drive/folders/1FE95g3u5Qh2b-W_Mrh0QBjMIXaC86mcT?usp=sharing",
        "ee_grad_proposals": "https://drive.google.com/drive/folders/1IwDgSRMe6Ok2DEFbt0LKlR4HNLIc_l1R?usp=sharing"
}

# =========================
# Helpers
# =========================

def main_menu_keyboard(chat_id):
    keyboard =  [
        [
            InlineKeyboardButton("💻 هندسة الحاسوب", callback_data="cse"), 
            InlineKeyboardButton("📡 هندسة الاتصالات", callback_data="te")
        ],
        [
            InlineKeyboardButton("🛠️ هندسة الميكانيك", callback_data="me"), 
            InlineKeyboardButton("⚙️ هندسة الميكاترونيكس", callback_data="me")
        ],
        [
            InlineKeyboardButton("⚡ الهندسة الكهربائية والأتمتة الصناعية", callback_data="ee")
        ],
        [
            InlineKeyboardButton("🏗 هندسة البناء", callback_data="ce"), 
            InlineKeyboardButton("🏢 الهندسة المدنية", callback_data="ce")
        ],
        [
            InlineKeyboardButton("📚 مشاريع تخرج", callback_data="grad")
        ],
        [
            InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq"),
            InlineKeyboardButton("شارك البوت", callback_data="share")
        ]
    ]
    if chat_id == TARGET_CHAT_ID:
        keyboard.append(
            [
                InlineKeyboardButton("لوحة التحكم", callback_data="dashboard")
            ]
        )
    return keyboard

def share_bot_keyboard():
    
    WHATSAPP_SHARE = "https://wa.me/?text=جرّب%20هذا%20البوت%20الجامعي%20👇%20https://t.me/IVR_Library_bot"
    FACEBOOK_SHARE = "https://www.facebook.com/sharer/sharer.php?u=https://t.me/IVR_Library_bot"
    TELEGRAM_SHARE = "https://t.me/share/url?url=https://t.me/IVR_Library_bot&text=جرّب%20هذا%20البوت%20الجامعي"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 شارك على واتساب", url=WHATSAPP_SHARE)],
        [InlineKeyboardButton("📘 شارك على فيسبوك", url=FACEBOOK_SHARE)],
        [InlineKeyboardButton("✈️ شارك على تيليجرام", url=TELEGRAM_SHARE)],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ])

def specialization_menu(spec_code: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📘 إجباري تخصص", callback_data=f"{spec_code}_dm"), 
            InlineKeyboardButton("📗 اختياري تخصص", callback_data=f"{spec_code}_do")
        ],
        [
            InlineKeyboardButton("📚 مواد مشتركة", callback_data=f"{spec_code}_shared_subjects")
        ],
        [
            InlineKeyboardButton("Roadmaps", callback_data=f"{spec_code}_roadmaps"), 
            InlineKeyboardButton("🔙 رجوع", callback_data="back_main")
        ]
    ])

def shared_subjects_menu(spec_code: str):
    
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📘 إجباري الجامعة", callback_data=f"{spec_code}_shared_um")
        ],
        [
            InlineKeyboardButton("📗 إجباري الكلية", callback_data=f"{spec_code}_shared_cm")
        ],
        [
            InlineKeyboardButton("📙 اختياري الجامعة", callback_data=f"{spec_code}_shared_uo")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data=spec_code.split("_")[0]),
            InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
        ]
    ])

def proj_probo_menu(spec_code: str):
    
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📂 مشاريع التخرج", url=GRAD_PROJECTS[f"{spec_code}_projects"])
        ],
        [
            InlineKeyboardButton("📝 مقدمات مشاريع التخرج", url=GRAD_PROJECTS[f"{spec_code}_proposals"])
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="grad"),
            InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
        ]
    ])

# =========================
# Commands
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    track_user(user.id)
    intro_text = (
        "👋 أهلاً بك في بوت IVR copilot من تطوير جمعية IVR الهندسية\n\n"
        "📌 طريقة استخدام البوت: \n\n"
        "• البوت يعمل بالكامل عبر الأزرار.\n\n"
        "• اختر تخصصك من القائمة الرئيسية.\n\n"
        "• ادخل إلى قسم للعثور على المقررات: اختراد ثم اختر نوع المادة.\n\n"
        "• داخل كل مادة ستجد التلاخيص، الشروحات، الكتب، الامتحانات وغيرها.\n\n"
        "• يمكنك دائمًا الرجوع باستخدام زر (رجوع).\n\n"
        "• لإعادة تشغيل البوت:  /start\n\n"
        "• محتويات البوت:  /cont\n\n"
        "• 💡 لإرسال ملاحظة أو اقتراح قم بكتابة الرسالة للبوت.\n\n"
        "• عن الجمعية:  /about\n\n"
        "👇 اختر من القائمة:"
    )

    

    await update.message.reply_text(
        intro_text,
        reply_markup=InlineKeyboardMarkup(main_menu_keyboard(chat_id)) #update, context
    )

async def inst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    track_user(user.id)
    await update.message.reply_text(
        "📘 هذا البوت تعليمي يعتمد على القوائم.\n"
        "تنقّل بين التخصصات والمواد باستخدام الأزرار فقط."
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    track_user(user.id)
    about_text = (
        "✳️ ما هي جمعية IVR\n\n"
        "⬅️ هي مؤسسة طلابية تطوعية غير ربحية مستقلة تقوم على تيسير أمور الطلبة في جامعة فلسطين التقنية (خضوري) ورفع مستواهم أكاديمياً ودينياً وثقافياً وعلمياً."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌐 موقع الجمعية", url="https://ivr-team-ptuk.github.io/IVR-Library/?fbclid=IwY2xjawNymGFleHRuA2FlbQIxMABicmlkETFMSGl6T3c4cVpQbWpuS2p5AR68bIpdoxosS9jmgwshDFGnri5PuCaE2fCbAJGlUuTNpUB3xavM77oyuWXnpA_aem_zRZUN5noXRofmBzQFgpyLQ")
        ],
        [
            InlineKeyboardButton("🏛 منصة كلية الهندسة والتكنولوجيا IVR", url="https://www.facebook.com/groups/395354431026877/")
        ],
        [
            InlineKeyboardButton("حساب الجمعية - فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100031851995367"),
            InlineKeyboardButton("حساب الجمعية - إنستغرام", url="https://www.instagram.com/ivr_ptuk/")
        ],
        [
            InlineKeyboardButton("اللجنة العلمية - فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100046123754881")
        ],
        [
            InlineKeyboardButton("اللجنة الثقافية – فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100092553221922/"),
            InlineKeyboardButton("اللجنة الثقافية – إنستغرام", url="https://www.instagram.com/ivr.cultural/")
        ],
        [
            InlineKeyboardButton("▶️ قناة اليوتيوب", url="https://youtube.com/@ivr_channel?si=UPQeWn_mKz28jnZB")
        ],
        # [InlineKeyboardButton("🤝 انضم_HERE")],
        [InlineKeyboardButton("📝 قدم مقترحاً", callback_data="note")],
        [
            InlineKeyboardButton("🏫 IVR NAJAH", url="https://www.facebook.com/groups/2416874278576851/")
        ],
        [
            InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
        ]
    ])

    await update.message.reply_text(
        about_text,
        reply_markup=keyboard
    )

# =========================
# Callback Buttons
# =========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    track_user(user.id)
    query = update.callback_query
    await query.answer()
    data = query.data

    # ---- Main specializations ----
    if data.endswith("shared_subjects"):
        await query.edit_message_text(
            text="📚 المواد المشتركة بين جميع التخصصات:",
            reply_markup=shared_subjects_menu(data)
        )
        
    elif data == "dashboard":
        await query.edit_message_text(
            text="لوحة التحكم:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("إحصائيات الاستخدام", callback_data = "users_analysis"), 
                    InlineKeyboardButton("خروج", callback_data = "back_main")
                ]
            ])
        )
    elif data == "users_analysis":
        await users_analysis(update, context)
    elif data.endswith("_shared_um"):
        await query.edit_message_text(
            text="📚 إجباري الجامعة:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("مهارات الحاسوب", url = "https://drive.google.com/drive/folders/1AqY3HGTmsEKJR-hUXoqR5-EeT-HE0HUe"), 
                    InlineKeyboardButton("مهارات الاتصال", url = "https://drive.google.com/drive/folders/1ag6esdUXaaFg8hKQRtdtTqjMIsPPLqxh")
                ],
                [
                    InlineKeyboardButton("اللغة العربية", url = "https://drive.google.com/drive/folders/16wiqvllo8uDoOt3mYA_tB_L8_DHmNG4F"), 
                    InlineKeyboardButton("اللغة الإنجليزية 1", url = "https://drive.google.com/drive/folders/1QbSzV5flY50kuT1IrtFu-DhwZ4fc0dv7")
                ],
                [
                    InlineKeyboardButton("الدراسات الإسلامية", url = "https://drive.google.com/drive/folders/1l_p-WrNOhr21VDdDE7FpNLy3QAbn1qg0"), 
                    InlineKeyboardButton("القضية الفلسطينية", url = "https://drive.google.com/drive/folders/1AsOgF_Dqp2LKbKnfNjw12fTcEsx8-DI0")
                ],
                [
                    InlineKeyboardButton("استدراكي اللغة الإنجليزية", url = "https://drive.google.com/drive/folders/1zoPLhWLfna2YHdZSQ5W2zMU9dDiiLq4I")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data.endswith("_shared_cm"):
        await query.edit_message_text(
            text="📚 إجباري الكلية:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("رسم هندسي", url = "https://drive.google.com/drive/folders/19yDHfznncH4DuqWh5SlCy2siAZpNm7PV?hl=ar"),
                    InlineKeyboardButton("مشغل هندسي", url = "https://drive.google.com/drive/folders/1xYwCFikleDJloKnOG1jV5xtz4NSBMunG?hl=ar"), 
                    InlineKeyboardButton("اقتصاد هندسي", url = "https://drive.google.com/drive/folders/1LiWsRZMwQH1LlKF513cy-umELAgankIO")
                ],
                [
                    InlineKeyboardButton("الكتابة التقنية وأخلاقيات المهنة", url = "https://drive.google.com/drive/folders/1AjAp3qXHr4jEpCIuSlJktcAyX4pyPOK6?hl=ar")
                ],
                [
                    InlineKeyboardButton("تفاضل وتكامل 1", url = "https://drive.google.com/drive/folders/1FJFRsOX9isi5FpqIt3UhsceQZfxmZcQS"),
                    InlineKeyboardButton("تفاضل وتكامل 2", url = "https://drive.google.com/drive/folders/1JpqO5Pa7P0xk0D6C1auVNDCy_yqFnmgl")
                ],
                [
                    InlineKeyboardButton("رياضيات هندسية 1", url = "https://drive.google.com/drive/folders/1p1uokT1-inoyoloh-AhYZ5GBmYiz1_UU"),
                    InlineKeyboardButton("رياضيات هندسية 2", url = "https://drive.google.com/drive/folders/16OqtFroWpAV0QgyVEIiIwrU0ICuoGoaj")
                ],
                [
                    InlineKeyboardButton("فيزياء عامة 1", url = "https://drive.google.com/drive/folders/1eTrvltnuqp8AHNQUS7JWffjC2ei9LAMM"),
                    InlineKeyboardButton("فيزياء عامة 2", url = "https://drive.google.com/drive/folders/1al3U6btk6IMrhDS-zC-uOYHkaF2YgkZ9")
                ],
                [
                    InlineKeyboardButton("مختبر فيزياء 1", url = "https://drive.google.com/drive/folders/1h_aqGgyD5V-IpG91KgUvCPec89FeSVtP?hl=ar"),
                    InlineKeyboardButton("مختبر فيزياء 2", url = "https://drive.google.com/drive/folders/1nO-MDLUo7-ihBxq-l-t2WG9au9ejWqWM?hl=ar")
                ],
                [
                    InlineKeyboardButton("كيمياء عامة 1", url = "https://drive.google.com/drive/folders/1_iO_Yk82kHH0bPz5I06lz1a8-2bt5o8N"),
                    InlineKeyboardButton("اللغة الإنجليزية 2", url = "https://drive.google.com/drive/folders/1byU064ptdQ1mAxMSA8-twk8F5QZIp7Sy")
                ],
                [
                    InlineKeyboardButton("مقدمة في منهجية البحث العلمي", url = "https://drive.google.com/drive/folders/1ACRINqfCFGBZpLQGHtWUWyF5bVbC3Wj0?hl=ar")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data.endswith("_shared_uo"):
        await query.edit_message_text(
            text="📚 اختياري الجامعة:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("الريادة والابداع", url = "https://drive.google.com/drive/folders/1BSYpLtfklUmW1UoimwokK-MZwGl99h4B"), 
                    InlineKeyboardButton("إسعافات أولية", url = "https://drive.google.com/drive/folders/1eMYmt_RpY6K-8xozQ83C3qtfc_iGLsLj")
                ],
                [
                    InlineKeyboardButton("الرياضة والصحة", url = "https://drive.google.com/drive/folders/1_epsNMs45Pdqvk0AdWMaWLYtd0zZ9M5K"), 
                    InlineKeyboardButton("الفكر الإسلامي", url = "https://drive.google.com/drive/folders/1tfqMI736xu9bFpete1wxmNVE1jr1tTl7")
                ],
                [
                    InlineKeyboardButton("القانون في حياتنا", url = "https://drive.google.com/drive/folders/1_syfDYEHmtduIWok1u_jnkFBQ6WbqjV_"), 
                    InlineKeyboardButton("تنشئة الأطفال", url = "https://drive.google.com/drive/folders/1uQKcXDGt03A3Y_1c63nd7IUhfNZgUe0U")
                ],
                [
                    InlineKeyboardButton("حضارة إسلامية", url = "https://drive.google.com/drive/folders/1z3q-13a_rOFO6dtZbMjAGwNEwCh2P1KV"), 
                    InlineKeyboardButton("حركة أسيرة", url = "https://drive.google.com/drive/folders/1-80OIWdDTtaapkyiURGmFpR4jLDg-UK_")
                ],
                [
                    InlineKeyboardButton("مقدمة في هندسة السيارات", url = "https://drive.google.com/drive/folders/1M6Ovliw7EJ9awE6Kg9oJuK4fG-EDTt5j"), 
                    InlineKeyboardButton("مهارات التواصل المهني", url = "https://drive.google.com/drive/folders/1ihs9BylIKUSQBIoRSWHxI18XTF2bbrmM?hl=ar")
                ],
                [
                    InlineKeyboardButton("مكافحة الفساد", url = "https://drive.google.com/drive/folders/1O-chfPMtuD-s2LBH9GW-H-x-qIYh6jBZ"), 
                    InlineKeyboardButton("قضايا معاصرة", url = "https://drive.google.com/drive/folders/1-9b_H2IMbZLU3mg_aw1MpicFsCZsR6vw")
                ],
                [
                    InlineKeyboardButton("اللغة التركية", url = "https://drive.google.com/drive/folders/1SgqSxvQruuFVIdOoYOw2tcDF3upC0jGC?hl=ar"), 
                    InlineKeyboardButton("المكتبة وطرق البحث", url = "https://drive.google.com/drive/folders/1X4AvmeV5CcQXvXmcsBqdmuiu_OK5WXOR")
                ],
                [
                    InlineKeyboardButton("اللغة العبرية", url = "https://drive.google.com/drive/folders/1FuWbM2ZHMSsf4Gnp1TxeVA9mTzeoAZ5Q?hl=ar"), 
                    InlineKeyboardButton("تاريخ القدس", url = "https://drive.google.com/drive/folders/1NMuX-KEWdye6nuYRTjb-qZk2aYwH0kwH?hl=ar")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    elif data == "grad":
        await query.edit_message_text(
            text="🎓 مشاريع التخرج\n\nاختر التخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("💻 هندسة الحاسوب", callback_data="cse_grad"), 
                    InlineKeyboardButton("📡 هندسة الاتصالات", callback_data="te_grad")
                ],
                [
                    InlineKeyboardButton("🛠️ هندسة الميكانيك", callback_data="me_grad"), 
                    InlineKeyboardButton("⚙️ هندسة الميكاترونيكس", callback_data="mee_grad")
                ],
                [
                    InlineKeyboardButton("⚡ الهندسة الكهربائية", callback_data="ee_grad"),
                    InlineKeyboardButton("🪫 هندسة الطاقة", callback_data="gee_grad")
                ],
                [
                    InlineKeyboardButton("🏗 هندسة البناء", callback_data="ce_grad"), 
                    InlineKeyboardButton("🏢 الهندسة المدنية", callback_data="cve_grad")
                ],
                [   
                    InlineKeyboardButton("🔙 رجوع", callback_data="back_main")
                ]
            ])
        )
    elif data.endswith("_grad"):
        titles = {
            "cse": "اختر مشروع/مقدمة مشروع:\n\n💻 هندسة الحاسوب",
            "me": "اختر مشروع/مقدمة مشروع:\n\n🛠️ هندسة الميكانيك",
            "mee": "اختر مشروع/مقدمة مشروع:\n\n⚙️ هندسة الميكاترونيكس",
            "ee": "اختر مشروع/مقدمة مشروع:\n\n⚡ الهندسة الكهربائية",
            "gee": "اختر مشروع/مقدمة مشروع:\n\n🪫 هندسة الطاقة",
            "te": "اختر مشروع/مقدمة مشروع:\n\n📡 هندسة الاتصالات",
            "ce": "اختر مشروع/مقدمة مشروع:\n\n🏗️ هندسة البناء",
            "cve": "اختر مشروع/مقدمة مشروع:\n\n🏢 الهندسة المدنية"
        }
        await query.edit_message_text(
            text=titles[data.split("_")[0]],
            reply_markup=proj_probo_menu(data)
        )

    elif data in ["cse", "me", "ee", "te", "ce", "mee", "ee", "cve"]:
        titles = {
            "cse": "💻 هندسة الحاسوب",
            "me": "⚙️ هندسة الميكانيك والميكاترونيكس",
            "mee": "⚙️ هندسة الميكانيك والميكاترونيكس",
            "ee": "⚡ الهندسة الكهربائية والأتمتة الصناعية",
            "eae": "⚡ الهندسة الكهربائية والأتمتة الصناعية",
            "te": "📡 هندسة الاتصالات",
            "ce": "🏗 هندسة البناء والهندسة المدنية",
            "cve": "🏗 هندسة البناء والهندسة المدنية"
        }

        await query.edit_message_text(
            text=titles[data],
            reply_markup=specialization_menu(data)
        )

    elif data=="cse_dm":
        await query.edit_message_text(
            text="حاسوب - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("برمجة الحاسوب", url = "https://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar"), 
                    InlineKeyboardButton("البرمجة الكينونية", url = "https://drive.google.com/drive/folders/16mlcz7332pqsXWDcVM45Ez9Hi8KE2DWN?hl=ar"), 
                    InlineKeyboardButton("تركيب البيانات", url = "https://drive.google.com/drive/folders/1MU9nY5LtI6_qzvvlIsM8p_JE9-OgYi7Z?hl=ar")],
                [
                    InlineKeyboardButton("م. تركيب البيانات", url = "https://drive.google.com/drive/folders/1eMTzUX_1TvhkoWctA64IsHP7nokKtTVa?hl=ar"), 
                    InlineKeyboardButton("تراكيب الحوسبة المتقطعة", url = "https://drive.google.com/drive/folders/1r19VoO7Jn3th47Yvv02xqp_j_cRIANer?hl=ar")
                ], 
                [
                    InlineKeyboardButton("نظم تشغيل", url = "https://drive.google.com/drive/folders/1h5UMPn2E9PKEbApKMgr5gw6fcQD75ICX?hl=ar"), 
                    InlineKeyboardButton("خوارزميات", url = "https://drive.google.com/drive/folders/1HW8jr8rkYG1mCTu5Hw7V9bu6XrlMLj1K?hl=ar"), 
                    InlineKeyboardButton("قواعد البيانات", url = "https://drive.google.com/drive/folders/1As24z-MhrkxUgOQCTvxulg3ZscQL2X01?hl=ar")
                ],
                [
                    InlineKeyboardButton("شبكات الحاسوب", url = "https://drive.google.com/drive/folders/1bHhvXwaW1gp1CnDiNqOpK8iuytzc5H31?hl=ar"), 
                    InlineKeyboardButton("م. قواعد البيانات", url = "https://drive.google.com/drive/folders/1gC2wrrVNaC2pFtTehECBQTq1YbVJ4fTW?hl=ar")
                ],
                [
                    InlineKeyboardButton("معمارية الحاسوب", url = "https://drive.google.com/drive/folders/1Ykp8VwEvfIgk0cJcLyZf6l8YY71fDftQ?hl=ar"), 
                    InlineKeyboardButton("م. شبكات الحاسوب", url = "https://drive.google.com/drive/folders/1y1D1FDgygSb0fZihJya49RzePjdp874u?hl=ar")
                ],
                [
                    InlineKeyboardButton("تحليل وتصميم أنظمة المعلومات", url = "https://drive.google.com/drive/folders/1oLU6aQTdXa7ktuODLajyWRrvO1AowfiZ?hl=ar")
                ],
                [
                    InlineKeyboardButton("م. أسمبلي", url = "https://drive.google.com/drive/folders/1Z8lWitiU9XDp5p8-fCKOvRklf4P0y7QT?hl=ar"), 
                    InlineKeyboardButton("أسمبلي", url = "https://drive.google.com/drive/folders/1Mar8liqfh9GtAuJt_3HLhvy1F9df9iuF?hl=ar"), 
                    InlineKeyboardButton("هندسة برمجيات", url = "https://drive.google.com/drive/folders/1I6Qon3_jvBG4KoGtmwQ1qBabzuA1ztvW?hl=ar")
                ],
                [
                    InlineKeyboardButton("التصميم المنطقي عالي المستوى", url = "https://drive.google.com/drive/folders/1cQhqZuOg05wOhLBfJCDErHo5Sdh9GWaD?hl=ar")
                ],
                [
                    InlineKeyboardButton("تقنيات الانترنت وتطبيقات الويب", url = "https://drive.google.com/drive/folders/1wz3InGxK3ZkUzeKVgACEB7k_lAP8Fyaa?hl=ar")
                ],
                [
                    InlineKeyboardButton("الذكاء الاصطناعي", url = "https://drive.google.com/drive/folders/1EGiAnJdtjmYP6q5WxbvOzz4rd0O6nf0I?hl=ar"), 
                    InlineKeyboardButton("برمجة الشبكات", url = "https://drive.google.com/drive/folders/1KGn9YDVnoZZVDPjfYa516ToWJHQZJmKm?hl=ar")
                ],
                [
                    InlineKeyboardButton("الدوائر الكهربائية", url = "https://drive.google.com/drive/folders/1Y4BPIHpd21iBm_9wSfDYPcyLFbBeU_kb"), 
                    InlineKeyboardButton("م. الدوائر الكهربائية", url = "https://drive.google.com/drive/folders/1oh7bNZxJtEows95EjCNRawxlfZ8SzZ8U?hl=ar")
                ],
                [
                    InlineKeyboardButton("إلكترونيات", url = "https://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb"), 
                    InlineKeyboardButton("م. إلكترونيات", url = "https://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar")
                ],
                [
                    InlineKeyboardButton("تصميم الدوائر المنطقية", url = "https://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI")
                ],
                [
                    InlineKeyboardButton("م. تصميم الدوائر المنطقية", url = "https://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar")
                ],
                [
                    InlineKeyboardButton("إلكترونيات رقمية", url = "https://drive.google.com/drive/folders/10BaqCIeCxxGmZFtNf0iHjLp0PGnXM3xe"), 
                    InlineKeyboardButton("الإشارات والنظم", url = "https://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0")
                ],
                [
                    InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", url = "https://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV")
                ],
                [
                    InlineKeyboardButton("أنظمة الاتصالات", url = "https://drive.google.com/drive/folders/12ZENHtxlaqjpYgV79NTBgDiNBqIqcfsn"), 
                    InlineKeyboardButton("معالجة الإشارات الرقمية", url = "https://drive.google.com/drive/folders/1uXoNhnC_6O_Z-0EdQxZ4YUXNd1q74YUd")
                ],
                [
                    InlineKeyboardButton("أنظمة التحكم 1", url = "https://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar"), 
                    InlineKeyboardButton("تحليل عددي", url = "https://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="cse"),
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data=="cse_do":
        await query.edit_message_text(
            text="حاسوب - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("مواضيع متقدمة في قواعد البيانات", url = "https://drive.google.com/drive/folders/1yz8LMm1E4ErufxXHsA2ZBXw29cThH8wN?usp=drive_link")
                ],
                [
                    InlineKeyboardButton("أنظمة الألياف الضوئية", url = "https://drive.google.com/drive/folders/13IlmE6sMct-gAdZxoTmhlZJxNJGGBjXN")
                ],
                [
                    InlineKeyboardButton("التشفير وأمن الشبكات", url = "https://drive.google.com/drive/folders/11QMuiAHOtzktbKzEdXJkfpxf6h84neqt?hl=ar"), 
                    InlineKeyboardButton("تنجيم البيانات", url = "https://drive.google.com/drive/folders/1yRaeasZdEedjtbgvAC2gY2c1JggQeAyL?hl=ar")
                ],
                [
                    InlineKeyboardButton("مواضيع خاصة في هندسة انظمة الحاسوب", url = "https://drive.google.com/drive/folders/1yz8LMm1E4ErufxXHsA2ZBXw29cThH8wN?usp=drive_link")
                ],
                [
                    InlineKeyboardButton("تعلم الآلة", url = "https://drive.google.com/drive/folders/1r9W75-GeMHrNeNT7KXF-r_zqBM7QyoLp?hl=ar"), 
                    InlineKeyboardButton("أنماط التصميم", url = "https://drive.google.com/drive/folders/1-KqrAUZeX7QYF4hHUqaDMnVMqLpFbx2k?hl=ar")
                ],
                [
                    InlineKeyboardButton("نظرية المعلومات والترميز (كودينج)", url = "https://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4")
                ],
                [
                    InlineKeyboardButton("المجسات ومحولات الطاقة (سنسور)", url = "https://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="cse"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    elif data=="te_dm":
        await query.edit_message_text(
            text="اتصالات - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("م. متحكمات دقيقة", url = "https://drive.google.com/drive/folders/1vdD5m2AxEr5W3QtIWu42SBdPf95wUND_?hl=ar"), 
                    InlineKeyboardButton("متحكمات دقيقة", url = "https://drive.google.com/drive/folders/15jlZjQKiTjJgMLO28f_h4u79IE5XYisr")
                ],
                [
                    InlineKeyboardButton("م. تصميم الدوائر المنطقية", url = "https://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar"), 
                    InlineKeyboardButton("تصميم الدوائر المنطقية", url = "https://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI")
                ],
                [
                    InlineKeyboardButton("م. إلكترونيات", url = "https://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar"), 
                    InlineKeyboardButton("إلكترونيات", url = "https://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb")
                ],
                [
                    InlineKeyboardButton("م. أنظمة تحكم 1", url = "https://drive.google.com/drive/folders/1iJuSOKY6c1LQ8oZ15ncKiaVxEOGlCHst?hl=ar"), 
                    InlineKeyboardButton("أنظمة تحكم 1", url = "https://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar")
                ],
                [
                    InlineKeyboardButton("م. دوائر كهربائية 1", url = "https://drive.google.com/drive/folders/1LOn0kXufvISSPDu3X7BiMSY3u5xnppWh?hl=ar"), 
                    InlineKeyboardButton("دوائر كهربائية 1", url = "https://drive.google.com/drive/folders/1zWr2kk4jznsqB2_VyDwUrlXAomX2ppJy")
                ],
                [
                    InlineKeyboardButton("م. دوائر كهربائية 2", url = "https://drive.google.com/drive/folders/1exrz303ktSkMn26VpbyR-dwwBH0MlEiL?hl=ar"), 
                    InlineKeyboardButton("دوائر كهربائية 2", url = "https://drive.google.com/drive/folders/11zw1ss3cgU3fX5xE3pd1bMAthrvUsasa")
                ],
                [
                    InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", url = "https://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV")
                ],
                [
                    InlineKeyboardButton("اتصالات تماثلية", url = "https://drive.google.com/drive/folders/1ZCQDftVAUNN6pufMmFz2MniZkK2OJvTp"), 
                    InlineKeyboardButton("اتصالات رقمية", url = "https://drive.google.com/drive/folders/1CCcNu0Y_DWD9lNSorrqAMnO6wfsNgWHV")
                ],
                [
                    InlineKeyboardButton("كهرومغناطيسية", url = "https://drive.google.com/drive/folders/11EZrizxPcbYY3xjGseDeOLLdFsIEunvM"), 
                    InlineKeyboardButton("الإشارات والنظم", url = "https://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0")
                ],
                [
                    InlineKeyboardButton("إلكترونيات متقدمة للاتصالات", url = "https://drive.google.com/drive/folders/1SOL5I1Im3twNrfKieLj0Kc4TWB30jowj")
                ],
                [
                    InlineKeyboardButton("برمجة حاسوب", url = "https://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar"), 
                    InlineKeyboardButton("شبكات حاسوب", url = "https://drive.google.com/drive/folders/11xXsav473CKMGf36TZdIOj39StalkIAt")
                ],
                [
                    InlineKeyboardButton("الصوتيات والأمواج الكهرومغناطيسية", url = "https://drive.google.com/drive/folders/1v7AWzoyTWJ5CADo-68oNMtp4hbXaCSfC")
                ],
                [
                    InlineKeyboardButton("الهوائيات وانتشار الأمواج", url = "https://drive.google.com/drive/folders/1zRh06odBIGSNOkxwZwa7ONJ5JiAa-KJC")
                ],
                [
                    InlineKeyboardButton("المجسات ومحولات الطاقة", url = "https://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm")
                ],
                [
                    InlineKeyboardButton("تحليل عددي", url = "https://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj"), 
                    InlineKeyboardButton("أنظمة الألياف الضوئية", url = "https://drive.google.com/drive/folders/13IlmE6sMct-gAdZxoTmhlZJxNJGGBjXN")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="te"),
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data=="te_do":
        await query.edit_message_text(
            text="اتصالات - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("تقنيات الإنترنت وتطبيقات الويب", url = "https://drive.google.com/drive/folders/1wz3InGxK3ZkUzeKVgACEB7k_lAP8Fyaa?hl=ar")
                ],
                [
                    InlineKeyboardButton("تركيب بيانات", url = "https://drive.google.com/drive/folders/1MU9nY5LtI6_qzvvlIsM8p_JE9-OgYi7Z?hl=ar"), 
                    InlineKeyboardButton("البرمجة الكينونية", url = "https://drive.google.com/drive/folders/16mlcz7332pqsXWDcVM45Ez9Hi8KE2DWN?hl=ar")
                ],
                [
                    InlineKeyboardButton("هندسة البرمجيات", url = "https://drive.google.com/drive/folders/1I6Qon3_jvBG4KoGtmwQ1qBabzuA1ztvW?hl=ar")
                ],
                [
                    InlineKeyboardButton("نظرية المعلومات والترميز (كودينج)", url = "https://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="te"),
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    elif data=="ee_dm":
        await query.edit_message_text(
            text="كهرباء - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("م. دوائر كهربائية 1", url = "https://drive.google.com/drive/folders/1LOn0kXufvISSPDu3X7BiMSY3u5xnppWh"),
                    InlineKeyboardButton("دوائر كهربائية 1", url = "https://drive.google.com/drive/folders/1zWr2kk4jznsqB2_VyDwUrlXAomX2ppJy")
                ],
                [
                    InlineKeyboardButton("م. دوائر كهربائية 2", url = "https://drive.google.com/drive/folders/1exrz303ktSkMn26VpbyR-dwwBH0MlEiL"),
                    InlineKeyboardButton("دوائر كهربائية 2", url = "https://drive.google.com/drive/folders/11zw1ss3cgU3fX5xE3pd1bMAthrvUsasa")
                ],
                [
                    InlineKeyboardButton("م. أنظمة تحكم 1", url = "https://drive.google.com/drive/folders/1iJuSOKY6c1LQ8oZ15ncKiaVxEOGlCHst"),
                    InlineKeyboardButton("أنظمة تحكم 1", url = "https://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F")
                ],
                [
                    InlineKeyboardButton("م. إلكترونيات 1", url = "https://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn"),
                    InlineKeyboardButton("إلكترونيات 1", url = "https://drive.google.com/drive/folders/1h94fbWvDZFPposGGpAUkfU0cNDVUN9jt")
                ],
                [
                    InlineKeyboardButton("إلكترونيات 2", url = "https://drive.google.com/drive/folders/12OecrqIQHpLo7TWKtbLwyFyQM1r0Jllh")
                ],
                [
                    InlineKeyboardButton("م. تصميم دوائر المنطقية", url = "https://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ"),
                    InlineKeyboardButton("تصميم الدوائر المنطقية", url = "https://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI")
                ],
                [
                    InlineKeyboardButton("م. إلكترونيات القدرة", url = "https://drive.google.com/drive/folders/1DWK1Q6nvE4cLGul2ZhvM5AyJsTP4FVEb"),
                    InlineKeyboardButton("إلكترونيات القدرة", url = "https://drive.google.com/drive/folders/1JGMx_EgOqtappXrCG8DRPhyjsqPsAS6k")
                ],
                [
                    InlineKeyboardButton("خطوط نقل الضغط العالي", url = "https://drive.google.com/drive/folders/1MfeVA8i88yBAZJPKBZWHdev122IEElhJ")
                ],
                [
                    InlineKeyboardButton("الإشارات والنظم", url = "https://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0"),
                    InlineKeyboardButton("كهرومغناطيسية", url = "https://drive.google.com/drive/folders/11EZrizxPcbYY3xjGseDeOLLdFsIEunvM")
                ],
                [
                    InlineKeyboardButton("م. أنظمة الاتصالات", url = "https://drive.google.com/drive/folders/1ysCfKkb8Pa-4DbvpVlu386-21TwIUEXr"),
                    InlineKeyboardButton("أنظمة الاتصالات", url = "https://drive.google.com/drive/folders/12ZENHtxlaqjpYgV79NTBgDiNBqIqcfsn")
                ],
                [
                    InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", url = "https://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV")
                ],
                [
                    InlineKeyboardButton("م. أنظمة التحكم المبرمجة", url = "https://drive.google.com/drive/folders/1XP4V02TjXmAtu2OPYnJ7lEOWC46-p655"),
                    InlineKeyboardButton("أنظمة التحكم المبرمجة", url = "https://drive.google.com/drive/folders/1-B9zlKvs7IebRZEungMNrQu6miLn0TS5")
                ],
                [
                    InlineKeyboardButton("أنظمة قوى كهربائية 1", url = "https://drive.google.com/drive/folders/11WaMIJF3MDdstrZkSidC_IzXjyl5ckqz"),
                    InlineKeyboardButton("آلات كهربائية 1", url = "https://drive.google.com/drive/folders/1-4IGpxohCaNpNa5UYyMiOrF3Lek7pjSC")
                ],
                [
                    InlineKeyboardButton("م. متحكمات دقيقة", url = "https://drive.google.com/drive/folders/1vdD5m2AxEr5W3QtIWu42SBdPf95wUND_"),
                    InlineKeyboardButton("متحكمات دقيقة", url = "https://drive.google.com/drive/folders/15jlZjQKiTjJgMLO28f_h4u79IE5XYisr")
                ],
                [
                    InlineKeyboardButton("استاتيكا وديناميكا", url = "https://drive.google.com/drive/folders/1xnChAL5DNph8HmQO-VNCnsYLDYLNV1kI"),
                    InlineKeyboardButton("برمجة الحاسوب", url = "https://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY")
                ],
                [
                    InlineKeyboardButton("م. قياسات كهربائية", url = "https://drive.google.com/drive/folders/17_RThMAo8ae6wsxj3ipgA9EP7Bbgm13j"),
                    InlineKeyboardButton("قياسات كهربائية", url = "https://drive.google.com/drive/folders/186kPiZPVbMlLaZ0nwvyWyfQY5NkDpXo3")
                ],
                [
                    InlineKeyboardButton("أنظمة قوى كهربائية 2", url = "https://drive.google.com/drive/folders/1-03rv3TLoqVkAKfXnZPBfsMWMGU4lgtP")
                ],
                [
                    InlineKeyboardButton("قيادة محركات التيار المستمر", url = "https://drive.google.com/drive/folders/15w_AciZLn7_70NyMI3pB0y4474CizpWs")
                ],
                [
                    InlineKeyboardButton("قيادة محركات التيار المتردد", url = "https://drive.google.com/drive/folders/1i6ME3YlM62Bgz0o8iNJhkSUBahNOY8zI")
                ],
                [
                    InlineKeyboardButton("م. آلات كهربائية", url = "https://drive.google.com/drive/folders/15bT6mBmbcNJuobmUny9ZhELwS3cZhLgr"),
                    InlineKeyboardButton("آلات كهربائية 2", url = "https://drive.google.com/drive/folders/1-7xQIuii6K_LeUI8-oXoV3jnlhmWhren")
                ],
                [
                    InlineKeyboardButton("م. التمديدات الكهربائية", url = "https://drive.google.com/drive/folders/1XLJzjKQ5vJqdgB_R4y33exik-xyLMGsQ"),
                    InlineKeyboardButton("التمديدات الكهربائية", url = "https://drive.google.com/drive/folders/1SdD9ZuTLwI-z25vYy5VWm4SFbpywVW0A")
                ],
                [
                    InlineKeyboardButton("تكنولوجيا الطاقة المستدامة 1", url = "https://drive.google.com/drive/folders/1-1JedAsjr-R-4zxXVIjNJcLYDQa7-IfU")
                ],
                [
                    InlineKeyboardButton("تكنولوجيا الطاقة المستدامة 2", url = "https://drive.google.com/drive/folders/1-1wBRd6PlW9G0Bh-_Z8sr44CDdCappYh")
                ],
                [
                    InlineKeyboardButton("م. تكنولوجيا الطاقة المستدامة 2", url = "https://drive.google.com/drive/folders/1hbpFRR5bXrOXPugYWqGfdwxEMU7Q-QUc")
                ],
                [
                    InlineKeyboardButton("هندسة محطات التوليد", url = "https://drive.google.com/drive/folders/1M6PrnSB542x8n2E-pkGbPBbfRZTGrhT4"),
                    InlineKeyboardButton("أنظمة التحكم الهيدروليكية", url = "https://drive.google.com/drive/folders/1CSKv_iJD7-W6kyIHRIwI9eWWYghwwSyO")
                ],
                [
                    InlineKeyboardButton("م. إلكترونيات", url = "https://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn"),
                    InlineKeyboardButton("إلكترونيات", url = "https://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb")
                ],
                [
                    InlineKeyboardButton("أنظمة الإشراف", url = "https://drive.google.com/drive/folders/1DBapVYC9KQGxuT3q0gNzd7c9fnCPUjZl"),
                    InlineKeyboardButton("تحليل عددي", url = "https://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj")
                ],
                [
                    InlineKeyboardButton("المجسات ومحولات الطاقة", url = "https://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm"),
                    InlineKeyboardButton("الديناميكا الحرارية", url = "https://drive.google.com/drive/folders/1bN_YHgvFio7VvALWn8bXUa1_tnReiY9T")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="ee"),
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data=="ee_do":
        await query.edit_message_text(
            text="كهرباء - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("أنظمة الحماية", url = "https://drive.google.com/drive/folders/1tdQgHmwxD75frzSgs0gZL2i6Ev0ghKIR"), 
                    InlineKeyboardButton("إلكترونيات متقدمة", url = "https://drive.google.com/drive/folders/1WJnZ2Jj9LmTrLo5alBkKXpHREBm9gwqc")
                ],
                [
                    InlineKeyboardButton("معالجة الإشارات الرقمية", url = "https://drive.google.com/drive/folders/1uXoNhnC_6O_Z-0EdQxZ4YUXNd1q74YUd")
                ],
                [
                    InlineKeyboardButton("تكنولوجيا الطاقة المتجددة", url = "https://drive.google.com/drive/folders/1-2ojI_P9gWfSOm7UxKr3Y23s0qcdV4of")
                ],
                [
                    InlineKeyboardButton("برمجة الشبكات", url = "https://drive.google.com/drive/folders/1bHhvXwaW1gp1CnDiNqOpK8iuytzc5H31?hl=ar"), 
                    InlineKeyboardButton("التحكم الرقمي", url = "https://drive.google.com/drive/folders/1XnZmiJhFT-b8Y8EixQivQ9oA9hdhLyd3")
                ],
                [
                    InlineKeyboardButton("نظرية المعلومات والترميز(كودينج)", url = "https://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4")
                ],
                [
                    InlineKeyboardButton("صوتيات وموجات كهرومغناطيسية", url = "https://drive.google.com/drive/folders/1v7AWzoyTWJ5CADo-68oNMtp4hbXaCSfC")
                ],
                [
                    InlineKeyboardButton("روبوتات", url = "https://drive.google.com/drive/folders/1xK1hqQs9vsDM7jbOrijhdHLJXk-IE9_2?hl=ar"), 
                    InlineKeyboardButton("تعلم الآلة", url = "https://drive.google.com/drive/folders/1g5aWIGVzM-vkrCgH4XU7pi-vA3TcfuJG")
                ],
                [
                    InlineKeyboardButton("إلكترونيات وكهرباء السيارات", url = "https://drive.google.com/drive/folders/1Ce-4LEeRYkrkMWQQqLeFZKdAAXD0y52Q?hl=ar")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="ee"),
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    elif data=="me_dm":
        await query.edit_message_text(
            text="ميكانيك وميكاترونيكس - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("م. دوائر كهربائية 1", url = "https://drive.google.com/drive/folders/1LOn0kXufvISSPDu3X7BiMSY3u5xnppWh?hl=ar"), 
                    InlineKeyboardButton("دوائر كهربائية 1", url = "https://drive.google.com/drive/folders/1zWr2kk4jznsqB2_VyDwUrlXAomX2ppJy")
                ],
                [
                    InlineKeyboardButton("م. دوائر كهربائية 2", url = "https://drive.google.com/drive/folders/1exrz303ktSkMn26VpbyR-dwwBH0MlEiL?hl=ar"), 
                    InlineKeyboardButton("دوائر كهربائية 2", url = "https://drive.google.com/drive/folders/11zw1ss3cgU3fX5xE3pd1bMAthrvUsasa")
                ],
                [
                    InlineKeyboardButton("م. أنظمة تحكم 1", url = "https://drive.google.com/drive/folders/1iJuSOKY6c1LQ8oZ15ncKiaVxEOGlCHst?hl=ar"), 
                    InlineKeyboardButton("أنظمة تحكم 1", url = "https://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar")
                ],
                [
                    InlineKeyboardButton("م. آلات كهربائية", url = "https://drive.google.com/drive/folders/15bT6mBmbcNJuobmUny9ZhELwS3cZhLgr?hl=ar"), 
                    InlineKeyboardButton("آلات كهربائية", url = "https://drive.google.com/drive/folders/11ONeQvvYjDBrCwFFbx7aiyu3U3GsbUDS")
                ],
                [
                    InlineKeyboardButton("م. إلكترونيات", url = "https://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar"),
                    InlineKeyboardButton("إلكترونيات", url = "https://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb")
                ],
                [
                    InlineKeyboardButton("م.تصميم دوائر منطقية", url = "https://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar"), 
                    InlineKeyboardButton("تصميم الدوائر المنطقية", url = "https://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI")
                ],
                [
                    InlineKeyboardButton("م. إلكترونيات القدرة", url = "https://drive.google.com/drive/folders/1DWK1Q6nvE4cLGul2ZhvM5AyJsTP4FVEb?hl=ar"), 
                    InlineKeyboardButton("إلكترونيات القدرة", url = "https://drive.google.com/drive/folders/1JGMx_EgOqtappXrCG8DRPhyjsqPsAS6k")
                ],
                [
                    InlineKeyboardButton("ديناميكا حرارية (2)", url = "https://drive.google.com/drive/folders/1GWqkFlf3Lmp1MkhnhhUyG-2DdBBwtza4"), 
                    InlineKeyboardButton("الديناميكا الحرارية", url = "https://drive.google.com/drive/folders/1bN_YHgvFio7VvALWn8bXUa1_tnReiY9T?hl=ar")
                ],
                [
                    InlineKeyboardButton("طرق التحليل بالعناصر المحددة", url = "https://drive.google.com/drive/folders/1AALjvwYQ8oaNTGzzKcA8HqxC-OpkpMc7")
                ],
                [
                    InlineKeyboardButton("تصميم عناصر الآلات (2)", url = "https://drive.google.com/drive/folders/1nHuXfMbq2DLREUD5YDoyU3uXf6TQCKOK")
                ],
                [
                    InlineKeyboardButton("تصميم أنظمة المحاكاة", url = "https://drive.google.com/drive/folders/15R8KhaTnuJvIxShKql4y3cugxlVAV_qI")
                ],
                [
                    InlineKeyboardButton("م. متحكمات دقيقة", url = "https://drive.google.com/drive/folders/1vdD5m2AxEr5W3QtIWu42SBdPf95wUND_?hl=ar"), 
                    InlineKeyboardButton("متحكمات دقيقة", url = "https://drive.google.com/drive/folders/15jlZjQKiTjJgMLO28f_h4u79IE5XYisr")
                ],
                [
                    InlineKeyboardButton("م. أنظمة التحكم المبرمجة", url = "https://drive.google.com/drive/folders/1XP4V02TjXmAtu2OPYnJ7lEOWC46-p655?hl=ar"), 
                    InlineKeyboardButton("أنظمة التحكم المبرمجة", url = "https://drive.google.com/drive/folders/1-B9zlKvs7IebRZEungMNrQu6miLn0TS5")
                ],
                [
                    InlineKeyboardButton("استاتيكا", url = "https://drive.google.com/drive/folders/1of0sj2JlxoN66lyYtOngQqWSAyOgz512?hl=ar"), 
                    InlineKeyboardButton("الإشارات والنظم", url = "https://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0")
                ],
                [
                    InlineKeyboardButton("م. ميكانيكا الموائع ونقل الحرارة", url = "https://drive.google.com/drive/folders/1mNBVBQ2PJphdASfDnOAoKDxv7fSjl8vu")
                ],
                [
                    InlineKeyboardButton("ديناميكا", url = "https://drive.google.com/drive/folders/1-MNDwo-cRXMKSI9_ROGBD7SKPM6NVAP_?hl=ar"), 
                    InlineKeyboardButton("أنظمة قوى كهربائية 1", url = "https://drive.google.com/drive/folders/11WaMIJF3MDdstrZkSidC_IzXjyl5ckqz")
                ],
                [
                    InlineKeyboardButton("الانتقال الحراري وميكانيكا الموائع", url = "https://drive.google.com/drive/folders/1bakFrIO5JDa-B2cmKoPAD3KrEwtb51Km")
                ],
                [
                    InlineKeyboardButton("م. قوة المواد", url = "https://drive.google.com/drive/folders/1PkT0nYMxy9VHOl56edAg61bInofLPZjJ?hl=ar"), 
                    InlineKeyboardButton("قوة المواد", url = "https://drive.google.com/drive/folders/12XA-itWG7wu9J4NOknCuZOvr4MErFmP6?hl=ar")
                ],
                [
                    InlineKeyboardButton("تصميم عناصر الآلات", url = "https://drive.google.com/drive/folders/1C_aonz113miO6AGZSrmvPY8TdtOuXCeY?hl=ar"), 
                    InlineKeyboardButton("نظرية الآلات", url = "https://drive.google.com/drive/folders/1wHhv1cIbZgYZb5dFVVOghvqld3U-ThvI?hl=ar")
                ],
                [
                    InlineKeyboardButton("تطبيقات هندسية باستخدام MATLAB", url = "https://drive.google.com/drive/folders/1hUfbichKsMgM_hNG4C1LE5Z_BvDIXHOw?hl=ar")
                ],
                [
                    InlineKeyboardButton("اهتزازات ميكانيكية", url = "https://drive.google.com/drive/folders/1C0om_juC5ywH095nHkePKzF3lbcMUBfl?hl=ar"), 
                    InlineKeyboardButton("برمجة الحاسوب", url = "https://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar")
                ],
                [
                    InlineKeyboardButton("تصميم أنظمة الميكاترونيكس", url = "https://drive.google.com/drive/folders/1fSO_OATeTpu3UMFRD_vElFaKnOahdZvF?hl=ar"), 
                    InlineKeyboardButton("أنظمة التحكم 2", url = "https://drive.google.com/drive/folders/1Oles6Pz1htv4YMXp84d5K7adtj_tYP0m?hl=ar")
                ],
                [
                    InlineKeyboardButton("الروبوتات", url = "https://drive.google.com/drive/folders/1xK1hqQs9vsDM7jbOrijhdHLJXk-IE9_2?hl=ar"), 
                    InlineKeyboardButton("المجسات ومحولات الطاقة", url = "https://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm")
                ],
                [
                    InlineKeyboardButton("م. ميكانيكا الموائع", url = "https://drive.google.com/drive/folders/1mNBVBQ2PJphdASfDnOAoKDxv7fSjl8vu?hl=ar"), 
                    InlineKeyboardButton("ميكانيكا الموائع", url = "https://drive.google.com/drive/folders/1bakFrIO5JDa-B2cmKoPAD3KrEwtb51Km?hl=ar")
                ],
                [
                    InlineKeyboardButton("م. دوائر كهربائية", url = "https://drive.google.com/drive/folders/1oh7bNZxJtEows95EjCNRawxlfZ8SzZ8U?hl=ar"), 
                    InlineKeyboardButton("دوائر كهربائية", url = "https://drive.google.com/drive/folders/1Y4BPIHpd21iBm_9wSfDYPcyLFbBeU_kb")
                ],
                [
                    InlineKeyboardButton("محرك الاحتراق الداخلي", url = "https://drive.google.com/drive/folders/1Y0MooV0syFRLXKRITA0aGHSUPXtvEfYp?hl=ar"), 
                    InlineKeyboardButton("تحليل عددي", url = "https://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj")
                ],
                [
                    InlineKeyboardButton("أنظمة التحكم الهيدرولوكية والهوائية", url = "https://drive.google.com/drive/folders/1CSKv_iJD7-W6kyIHRIwI9eWWYghwwSyO?hl=ar")
                ],
                [
                    InlineKeyboardButton("م. قياسات كهربائية", url = "https://drive.google.com/drive/folders/17_RThMAo8ae6wsxj3ipgA9EP7Bbgm13j?hl=ar"), 
                    InlineKeyboardButton("قياسات كهربائية", url = "https://drive.google.com/drive/folders/186kPiZPVbMlLaZ0nwvyWyfQY5NkDpXo3")
                ],
                [
                    InlineKeyboardButton("إلكترونيات وكهرباء السيارات", url = "https://drive.google.com/drive/folders/1Ce-4LEeRYkrkMWQQqLeFZKdAAXD0y52Q?hl=ar")
                ],
                [
                    InlineKeyboardButton("أنظمة المركبات", url = "https://drive.google.com/drive/folders/1Mnx-_8RpYndH5kmGxfAiQCzMH6uEoLD0"), 
                    InlineKeyboardButton("تكييف وتبريد", url = "https://drive.google.com/drive/folders/1DE2IC8WXxwLLtc709sw-l7X5WX6Y8CUn")
                ],
                [
                    InlineKeyboardButton("ديناميكا واهتزازت المركبات", url = "https://drive.google.com/drive/folders/1K8QD7U9duW_VY1XS9YxPjBucSPLqAYLd?hl=ar")
                ],
                [
                    InlineKeyboardButton("م. ديناميكا واهتزازت المركبات", url = "https://drive.google.com/drive/folders/1MfkQKhqoOTekK-MZNhhZIZtvezQAB5UY")
                ],
                [
                    InlineKeyboardButton("م. التمديدات الكهربائية", url = "https://drive.google.com/drive/folders/1XLJzjKQ5vJqdgB_R4y33exik-xyLMGsQ?hl=ar"), 
                    InlineKeyboardButton("التمديدات الكهربائية", url = "https://drive.google.com/drive/folders/1SdD9ZuTLwI-z25vYy5VWm4SFbpywVW0A")
                ],
                [
                    InlineKeyboardButton("مشغل سيارات 2", url = "https://drive.google.com/drive/folders/11tfyUh-4zC4zDQWPvYVsLVnFkyPS5xna?hl=ar"), 
                    InlineKeyboardButton("هندسة السلامة", url = "https://drive.google.com/drive/folders/1l0ORYZhMVxUJyQTHce47aAnSlPwLvEvQ?hl=ar")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="me"),
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data=="me_do":
        await query.edit_message_text(
            text="ميكانيك وميكاترونيكس - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ديناميكا واهتزازات المركبات", url = "https://drive.google.com/drive/folders/1K8QD7U9duW_VY1XS9YxPjBucSPLqAYLd?hl=ar")
                ],
                [
                    InlineKeyboardButton("مختبر ديناميكا واهتزازات المركبات", url = "https://drive.google.com/drive/folders/1MfkQKhqoOTekK-MZNhhZIZtvezQAB5UY")
                ],
                [
                    InlineKeyboardButton("الإشارات والنظم", url = "https://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0")
                ],
                [
                    InlineKeyboardButton("معالجة الإشارات الرقمية DSP", url = "https://drive.google.com/drive/folders/1uXoNhnC_6O_Z-0EdQxZ4YUXNd1q74YUd")
                ],
                [
                    InlineKeyboardButton("المجسات ومحولات الطاقة Sensors", url = "https://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm")
                ],
                [
                    InlineKeyboardButton("إلكترونيات وكهرباء السيارات", url = "https://drive.google.com/drive/folders/1Ce-4LEeRYkrkMWQQqLeFZKdAAXD0y52Q?hl=ar")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="me"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    elif data=="ce_dm":
        await query.edit_message_text(
            text="بناء ومدني - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", url = "https://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV")
                ],
                [
                    InlineKeyboardButton("برمجة الحاسوب", url = "https://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar"), 
                    InlineKeyboardButton("رسم هندسي", url = "https://drive.google.com/drive/folders/19yDHfznncH4DuqWh5SlCy2siAZpNm7PV?hl=ar")
                ],
                [
                    InlineKeyboardButton("ديناميكا", url = "https://drive.google.com/drive/folders/1-MNDwo-cRXMKSI9_ROGBD7SKPM6NVAP_?hl=ar"), 
                    InlineKeyboardButton("استاتيكا", url = "https://drive.google.com/drive/folders/1of0sj2JlxoN66lyYtOngQqWSAyOgz512?hl=ar")
                ],
                [
                    InlineKeyboardButton("الانتقال الحراري وميكانيكا الموائع", url = "https://drive.google.com/drive/folders/1bakFrIO5JDa-B2cmKoPAD3KrEwtb51Km")
                ],
                [
                    InlineKeyboardButton("مختبر قوة المواد", url = "https://drive.google.com/drive/folders/1PkT0nYMxy9VHOl56edAg61bInofLPZjJ?hl=ar"), 
                    InlineKeyboardButton("قوة المواد", url = "https://drive.google.com/drive/folders/12XA-itWG7wu9J4NOknCuZOvr4MErFmP6?hl=ar")
                ],
                [
                    InlineKeyboardButton("مختبر مساحة", url = "https://drive.google.com/drive/folders/147vtL8IEuffnW894fydKz3HC57wqs4K8?hl=ar"), 
                    InlineKeyboardButton("مساحة", url = "https://drive.google.com/drive/folders/1UNzOPplXbdtNfQ7Hc7T7V-4qssHVuvVX")
                ],
                [
                    InlineKeyboardButton("تكنولوجيا مواد البناء", url = "https://drive.google.com/drive/folders/1v-0vw0rBRBSGPYGxAJrpc_a1gkZfoUHF")
                ],
                [
                    InlineKeyboardButton("مختبر ميكانيكا التربة", url = "https://drive.google.com/drive/folders/1BiiYgkqVilFnmj2r8Z4owORtDybpkrwL?hl=ar"), 
                    InlineKeyboardButton("ميكانيكا التربة", url = "https://drive.google.com/drive/folders/1lw3EhR-awYXRyUYCxmXaG_wFDVjgrl9j")
                ],
                [
                    InlineKeyboardButton("خرسانة 2", url = "https://drive.google.com/drive/folders/1iQG2Cqnc2jPt15f3z5jQwujfOG19-O5o"), 
                    InlineKeyboardButton("خرسانة 1", url = "https://drive.google.com/drive/folders/1twqVEYdlihVy-pXoaENHWgDYBeEsk39w")
                ],
                [
                    InlineKeyboardButton("الإدارة المستدامة لمخلفات البيئة", url = "https://drive.google.com/drive/folders/1Ki6ye0KJphwDJfgIQCMecp4qzn8tiWlj")
                ],
                [
                    InlineKeyboardButton("تكنولوجيا الإنارة والتمديدات الكهربائية", url = "https://drive.google.com/drive/folders/1_cgibeUqX1ZYi4iA7EPJ-AyAv6N90qFR")
                ],
                [
                    InlineKeyboardButton("تصميم رصفات", url = "https://drive.google.com/drive/folders/1fs_TN7ub9-ZdtNtLiagHLCxXThOBaZgd"), 
                    InlineKeyboardButton("التدفئة والتكييف والتبريد", url = "https://drive.google.com/drive/folders/1DE2IC8WXxwLLtc709sw-l7X5WX6Y8CUn")
                ],
                [
                    InlineKeyboardButton("المباني صديقة البيئة", url = "https://drive.google.com/drive/folders/1_g-4BCGH3h78EOj3IJ7VdqMaE1EQxGpD"), 
                    InlineKeyboardButton("هندسة أساسات", url = "https://drive.google.com/drive/folders/15eXO9z_FU52y5WvWYWV2M-yndHtAr2dg")
                ],
                [
                    InlineKeyboardButton("أنظمة توزيع المياه وأنظمة الصرف الصحي", url = "https://drive.google.com/drive/folders/19sS7-CyxlqUJhiiy-BBPPqqQVTrTiBVK")
                ],
                [
                    InlineKeyboardButton("مختبر ميكانيكا الموائع ونقل الحرارة", url = "https://drive.google.com/drive/folders/1mNBVBQ2PJphdASfDnOAoKDxv7fSjl8vu")
                ],
                [
                    InlineKeyboardButton("هيدروليك", url = "https://drive.google.com/drive/folders/18fnbj1910Slou4YGHiyexMzPpuAK3OIp"), 
                    InlineKeyboardButton("إنشاءات", url = "https://drive.google.com/drive/folders/1kiHt-qNjdTM1sK015rZg7an8fykpiL10")
                ],
                [
                    InlineKeyboardButton("مواصفات وعقود وحساب كميات", url = "https://drive.google.com/drive/folders/1k_Rhz3YKz7n21cI4y_cockp6zr3KGPgC")
                ],
                [
                    InlineKeyboardButton("الإدارة الهندسية وضبط الجودة", url = "https://drive.google.com/drive/folders/1CnhE5_nTugvMnTGc3b61NPZ8JLwN_cIx")
                ],
                [
                    InlineKeyboardButton("تحليل إنشاءات 2", url = "https://drive.google.com/drive/folders/1F7yclgmoqsaX5RiCV3p3P-Y4J8AddTv1"), 
                    InlineKeyboardButton("تحليل إنشاءات 1", url = "https://drive.google.com/drive/folders/1j6um544BSHP0g-iePoxlLaUiMwNC3HOw")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="ce"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data=="ce_do":
        await query.edit_message_text(
            text="بناء ومدني - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("تصميم رصفات", url = "https://drive.google.com/drive/folders/1fs_TN7ub9-ZdtNtLiagHLCxXThOBaZgd")
                ],
                [
                    InlineKeyboardButton("مقدمة في منهجية البحث العلمي", url = "https://drive.google.com/drive/folders/1ACRINqfCFGBZpLQGHtWUWyF5bVbC3Wj0?hl=ar")
                ],
                [
                    InlineKeyboardButton("منشآت معدنية 2", url = "https://drive.google.com/drive/folders/1GdvnmWUXeYUpzLBty0lqOJkUMJuVkSP6")
                ],
                [
                    InlineKeyboardButton("خرسانة 3", url = "https://drive.google.com/drive/folders/1H7-AHGn7xrFhN2bIUoadzEr0aUD6VEq5")
                ],
                [
                    InlineKeyboardButton("تقييم الأثر البيئي", url = "https://drive.google.com/drive/folders/10_qN-SPXs1LvtaabsBMGQAARc2h9wV8g")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="ce"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    # ---- Roadmaps ----
    elif data == "cse_roadmaps":
        await query.edit_message_text(
            text="🗺 Roadmaps – هندسة الحاسوب",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🤖 AI & Machine Learning", url = "https://roadmap.sh/machine-learning")
                ],
                [
                    InlineKeyboardButton("📊 Data Science", url = "https://roadmap.sh/data-engineer"), 
                    InlineKeyboardButton("🤖 Robotics", url = "https://qr1.me-qr.com/mobile/pdf/d1770eda-eaec-47c7-aefe-d6b04597d1d9")
                ],
                [
                    InlineKeyboardButton("🔐 Cybersecurity", url = "https://roadmap.sh/cyber-security"), 
                    InlineKeyboardButton("🌐 Full Stack Developer", url = "https://roadmap.sh/full-stack")
                ],
                [
                    InlineKeyboardButton("🎨 Frontend", url = "https://roadmap.sh/frontend"), 
                    InlineKeyboardButton("🧠 Backend", url = "https://roadmap.sh/backend")
                ],
                [
                    InlineKeyboardButton("📱 iOS Dev", url = "https://roadmap.sh/ios"), 
                    InlineKeyboardButton("🧪 QA", url = "https://roadmap.sh/qa"), InlineKeyboardButton("🖌 UX", url = "https://roadmap.sh/ux-design")
                ],
                [
                    InlineKeyboardButton("📱 Android Dev", url = "https://roadmap.sh/android"), 
                    InlineKeyboardButton("🎮 Game Developer", url = "https://roadmap.sh/game-developer")
                ],
                [
                    InlineKeyboardButton("⚙ Low Level Programming", url = "https://qr1.me-qr.com/mobile/pdf/42137ab5-0755-4824-9f23-707f8f2e3df0")
                ],
                [
                    InlineKeyboardButton("⚡more tracks roadmaps⚡", url = "https://roadmap.sh")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="cse"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    elif data == "about":
        await query.edit_message_text(
            text =
            "✳️ ما هي جمعية IVR\n\n⬅️ هي مؤسسة طلابية تطوعية غير ربحية مستقلة تقوم على تيسير أمور الطلبة في جامعة فلسطين التقنية (خضوري) ورفع مستواهم أكاديمياً ودينياً وثقافياً وعلمياً.",

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🌐 موقع الجمعية", url="https://ivr-team-ptuk.github.io/IVR-Library/?fbclid=IwY2xjawNymGFleHRuA2FlbQIxMABicmlkETFMSGl6T3c4cVpQbWpuS2p5AR68bIpdoxosS9jmgwshDFGnri5PuCaE2fCbAJGlUuTNpUB3xavM77oyuWXnpA_aem_zRZUN5noXRofmBzQFgpyLQ")
                ],
                [
                    InlineKeyboardButton("🏛 منصة كلية الهندسة والتكنولوجيا IVR", url="https://www.facebook.com/groups/395354431026877/")
                ],
                [
                    InlineKeyboardButton("حساب الجمعية - فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100031851995367"),
                    InlineKeyboardButton("حساب الجمعية - إنستغرام", url="https://www.instagram.com/ivr_ptuk/")
                ],
                [
                    InlineKeyboardButton("اللجنة العلمية - فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100046123754881")
                ],
                [
                    InlineKeyboardButton("اللجنة الثقافية – فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100092553221922/"),
                    InlineKeyboardButton("اللجنة الثقافية – إنستغرام", url="https://www.instagram.com/ivr.cultural/")
                ],
                [
                    InlineKeyboardButton("▶️ قناة اليوتيوب", url="https://youtube.com/@ivr_channel?si=UPQeWn_mKz28jnZB")
                ],
                # [InlineKeyboardButton("🤝 انضم_HERE")],
                [InlineKeyboardButton("📝 قدم مقترحاً", callback_data="note")],
                [
                    InlineKeyboardButton("🏫 IVR NAJAH", url="https://www.facebook.com/groups/2416874278576851/")
                ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="faq"),
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
        # await query.message.reply_text(
        #     "🗺 Roadmaps – هندسة الحاسوب",
        #     reply_markup=InlineKeyboardMarkup([
        #         [InlineKeyboardButton(, InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
        #     ])
        # )

    # ---- FAQ ----
    elif data == "faq":
        keyboard = [
            [
                InlineKeyboardButton("🏫 عن الجامعة", callback_data="faq_university"), 
                InlineKeyboardButton("🎓 عن المنح", callback_data="faq_scholarships"), 
                InlineKeyboardButton("👨‍🏫 عن المدرسين", callback_data="faq_teachers")
            ],
            [
                InlineKeyboardButton("📚 عن الدراسة وطرقها", callback_data="faq_study"), 
                InlineKeyboardButton("🐣 أسئلة سنافر", callback_data="faq_freshmen"), 
                InlineKeyboardButton("💡 نصائح", callback_data="faq_tips")
            ],
            [
                InlineKeyboardButton("👥 عنا", callback_data="about"),
                InlineKeyboardButton("🔗 روابط هامة", callback_data="external_links")
            ],
            [
                InlineKeyboardButton("🔙 رجوع", callback_data="back_main")
            ]
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
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="faq"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data == "external_links":
        await query.edit_message_text(
            text="🔗 روابط هامة:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🏢 موقع الجامعة", url = "https://ptuk.edu.ps/ar/"),
                    InlineKeyboardButton("📝 موقع الجمعية", url = "https://ivr-team-ptuk.github.io/IVR-Library/")
                ],
                [
                    InlineKeyboardButton("🏢 البورتال", url = "https://edugate.ptuk.edu.ps/faces/ui/pages/student/index.xhtml"),
                    InlineKeyboardButton("🎓 المودل", url = "https://lms.ptuk.edu.ps/login/index.php?loginredirect=1")
                ],
                [
                    InlineKeyboardButton("📚 الخطط الدراسية الرسمية", url = "https://edugate.ptuk.edu.ps/faces/ui/pages/guest/plan/index.xhtml")
                ],
                [
                    InlineKeyboardButton("📚 الخطط الاسترشادية الشجرية", url = "https://drive.google.com/drive/folders/1BTQwIUQfj594V4cTDpI6EAbUkzaJ3PXo?usp=drive_link")
                ],
                [
                    InlineKeyboardButton("📧 أرقام وإيميلات الدكاترة", url = "https://drive.google.com/file/d/1zuK-Y8qVAxBH_XWaNqOu2wQEkKQYMfxh/view")
                ],
                [
                    InlineKeyboardButton("🗓️ التقويم الأكاديمي", url = "https://ptuk.edu.ps/ar/academic-calendar.php")
                ],
                # [
                #     InlineKeyboardButton("🔗 روابط هامة", url = "")
                # ],
                # [
                #     InlineKeyboardButton("🔗 روابط هامة", url = "")
                # ],
                # [
                #     InlineKeyboardButton("🔗 روابط هامة", url = "")
                # ],
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="faq"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
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
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="faq"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
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
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="faq"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
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
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="faq"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )
    elif data == "faq_tips":
        await query.edit_message_text(
            text="💡 نصائح:\n\n"
                 "• لا تؤجل الدراسة\n"
                 "• تابع التلاخيص\n"
                 "• اسأل ولا تتردد",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔙 رجوع", callback_data="faq"), 
                    InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")
                ]
            ])
        )

    # ---- Back to main ----
    elif data == "back_main":
        await query.edit_message_text(
            text=
            "👋 أهلاً بك في بوت IVR copilot من تطوير جمعية IVR الهندسية\n\n"
            "📌 طريقة استخدام البوت: \n\n"
            "• البوت يعمل بالكامل عبر الأزرار.\n\n"
            "• اختر تخصصك من القائمة الرئيسية.\n\n"
            "• ادخل إلى قسم المواد ثم اختر نوع المادة.\n\n"
            "• يمكنك الوصول إلى مشاريع التخرج من القائمة الرئيسية.\n\n"
            "• يمكنك دائمًا الرجوع باستخدام زر (رجوع).\n\n"
            "• لإعادة تشغيل البوت:  /start\n\n"
            "• محتويات البوت:  /cont\n\n"
            "• 💡 لإرسال ملاحظة أو اقتراح قم بكتابة الرسالة للبوت.\n\n"
            "• عن الجمعية:  /about\n\n"
            "👇 اختر من القائمة:",
            reply_markup=InlineKeyboardMarkup(main_menu_keyboard(chat_id))
        )

    elif data == "share":
        await query.edit_message_text(
            text= "شارك البوت:",
        reply_markup=share_bot_keyboard()
        )
# =========================
# Notes forwarding
# =========================

async def get_or_create_topic(context, user):
    topics = load_topics()
    user_id = str(user.id)

    if user_id in topics:
        return topics[user_id]["thread_id"]

    # إنشاء Topic جديد
    topic = await context.bot.create_forum_topic(
        chat_id=TARGET_CHAT_ID,
        name=f"{user.full_name}"
    )

    topics[user_id] = {
        "thread_id": topic.message_thread_id,
        "name": user.full_name
    }
    save_topics(topics)

    return topic.message_thread_id

async def copy_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    
    if not update.message:
        return

    if user.is_bot:
        return

    # تجاهل المجموعات
    if msg.chat.type != "private":
        return

    thread_id = await get_or_create_topic(context, user)
    prefix = (
        f"📩 رسالة جديدة\n\n"
        f"👤 الاسم: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"🔗 Username: @{user.username if user.username else '—'}\n"
        "──────────────\n"
    )

    send_kwargs = {
        "chat_id": TARGET_CHAT_ID,
        "message_thread_id": thread_id
    }

    if msg.text:
        sent = await context.bot.send_message(
            text=prefix + msg.text,
            **send_kwargs
        )
    elif msg.photo:
        sent = await context.bot.send_photo(
            photo=msg.photo[-1].file_id,
            caption=prefix + (msg.caption or ""),
            **send_kwargs
        )
    elif msg.document:
        sent = await context.bot.send_document(
            document=msg.document.file_id,
            caption=prefix + (msg.caption or ""),
            **send_kwargs
        )
    elif msg.video:
        sent = await context.bot.send_video(
            video=msg.video.file_id,
            caption=prefix + (msg.caption or ""),
            **send_kwargs
        )
    elif msg.audio:
        sent = await context.bot.send_audio(
            audio=msg.audio.file_id,
            caption=prefix + (msg.caption or ""),
            **send_kwargs
        )
    elif msg.voice:
        sent = await context.bot.send_voice(
            voice=msg.voice.file_id,
            caption=prefix,
            **send_kwargs
        )
    else:
        sent = await context.bot.send_message(
            text=prefix + "⚠️ نوع رسالة غير مدعوم",
            **send_kwargs
        )
    # ربط رسالة المشرف بالمستخدم
    context.bot_data[sent.message_id] = user.id
    
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    track_user(user.id)
    if msg.chat_id != TARGET_CHAT_ID:
        await copy_all_messages(update, context)
        return
    if not msg.reply_to_message:
        return

    replied_id = msg.reply_to_message.message_id
    target_user_id = context.bot_data.get(replied_id)

    if not target_user_id:
        return

    await msg.copy(chat_id=target_user_id)

# =========================
# Main
# =========================

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("inst", inst))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.ALL,handle_admin_reply))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
