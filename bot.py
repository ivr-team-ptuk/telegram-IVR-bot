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

SUBJECT_LINKS = { 

    # هندسة البناء – إجباري تخصص
    "ce_dm_prob": "🔗 كل ما يخص مادة الاحتمالات والمتغيرات العشوائية:\nhttps://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV",
    "ce_dm_prog": "🔗 كل ما يخص مادة برمجة الحاسوب:\nhttps://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar",
    "ce_dm_stat": "🔗 كل ما يخص مادة استاتيكا:\nhttps://drive.google.com/drive/folders/1of0sj2JlxoN66lyYtOngQqWSAyOgz512?hl=ar",
    "ce_dm_dyn": "🔗 كل ما يخص مادة ديناميكا:\nhttps://drive.google.com/drive/folders/1-MNDwo-cRXMKSI9_ROGBD7SKPM6NVAP_?hl=ar",
    "ce_dm_heat": "🔗 كل ما يخص مادة الانتقال الحراري وميكانيكا الموائع:\nhttps://drive.google.com/drive/folders/1bakFrIO5JDa-B2cmKoPAD3KrEwtb51Km",
    "ce_dm_matstr": "🔗 كل ما يخص مادة قوة المواد:\nhttps://drive.google.com/drive/folders/12XA-itWG7wu9J4NOknCuZOvr4MErFmP6?hl=ar",
    "ce_dm_labmat": "🔗 كل ما يخص مادة مختبر قوة المواد:\nhttps://drive.google.com/drive/folders/1PkT0nYMxy9VHOl56edAg61bInofLPZjJ?hl=ar",
    "ce_dm_draw": "🔗 كل ما يخص مادة رسم هندسي:\nhttps://drive.google.com/drive/folders/19yDHfznncH4DuqWh5SlCy2siAZpNm7PV?hl=ar",
    "ce_dm_survey": "🔗 كل ما يخص مادة مساحة:\nhttps://drive.google.com/drive/folders/1UNzOPplXbdtNfQ7Hc7T7V-4qssHVuvVX",
    "ce_dm_labsur": "🔗 كل ما يخص مادة مختبر مساحة:\nhttps://drive.google.com/drive/folders/147vtL8IEuffnW894fydKz3HC57wqs4K8?hl=ar",
    "ce_dm_tech": "🔗 كل ما يخص مادة تكنولوجيا مواد البناء:\nhttps://drive.google.com/drive/folders/1v-0vw0rBRBSGPYGxAJrpc_a1gkZfoUHF",
    "ce_dm_soil": "🔗 كل ما يخص مادة ميكانيكا التربة:\nhttps://drive.google.com/drive/folders/1lw3EhR-awYXRyUYCxmXaG_wFDVjgrl9j",
    "ce_dm_labsoil": "🔗 كل ما يخص مادة مختبر ميكانيكا التربة:\nhttps://drive.google.com/drive/folders/1BiiYgkqVilFnmj2r8Z4owORtDybpkrwL?hl=ar",
    "ce_dm_conc1": "🔗 كل ما يخص مادة خرسانة 1:\nhttps://drive.google.com/drive/folders/1twqVEYdlihVy-pXoaENHWgDYBeEsk39w",
    "ce_dm_conc2": "🔗 كل ما يخص مادة خرسانة 2:\nhttps://drive.google.com/drive/folders/1iQG2Cqnc2jPt15f3z5jQwujfOG19-O5o",
    "ce_dm_env": "🔗 كل ما يخص مادة الإدارة المستدامة لمخلفات البيئة:\nhttps://drive.google.com/drive/folders/1Ki6ye0KJphwDJfgIQCMecp4qzn8tiWlj",
    "ce_dm_light": "🔗 كل ما يخص مادة تكنولوجيا الإنارة والتمديدات الكهربائية:\nhttps://drive.google.com/drive/folders/1_cgibeUqX1ZYi4iA7EPJ-AyAv6N90qFR",
    "ce_dm_hvac": "🔗 كل ما يخص مادة التدفئة والتكييف والتبريد:\nhttps://drive.google.com/drive/folders/1DE2IC8WXxwLLtc709sw-l7X5WX6Y8CUn",
    "ce_dm_pave": "🔗 كل ما يخص مادة تصميم رصفات:\nhttps://drive.google.com/drive/folders/1fs_TN7ub9-ZdtNtLiagHLCxXThOBaZgd",
    "ce_dm_found": "🔗 كل ما يخص مادة هندسة أساسات:\nhttps://drive.google.com/drive/folders/15eXO9z_FU52y5WvWYWV2M-yndHtAr2dg",
    "ce_dm_green": "🔗 كل ما يخص مادة المباني صديقة البيئة:\nhttps://drive.google.com/drive/folders/1_g-4BCGH3h78EOj3IJ7VdqMaE1EQxGpD",
    "ce_dm_water": "🔗 كل ما يخص مادة أنظمة توزيع المياه وأنظمة الصرف الصحي:\nhttps://drive.google.com/drive/folders/19sS7-CyxlqUJhiiy-BBPPqqQVTrTiBVK",
    "ce_dm_labheat": "🔗 كل ما يخص مادة مختبر ميكانيكا الموائع ونقل الحرارة:\nhttps://drive.google.com/drive/folders/1mNBVBQ2PJphdASfDnOAoKDxv7fSjl8vu",
    "ce_dm_const": "🔗 كل ما يخص مادة إنشاءات:\nhttps://drive.google.com/drive/folders/1kiHt-qNjdTM1sK015rZg7an8fykpiL10",
    "ce_dm_hyd": "🔗 كل ما يخص مادة هيدروليك:\nhttps://drive.google.com/drive/folders/18fnbj1910Slou4YGHiyexMzPpuAK3OIp",
    "ce_dm_spec": "🔗 كل ما يخص مادة مواصفات وعقود وحساب كميات:\nhttps://drive.google.com/drive/folders/1k_Rhz3YKz7n21cI4y_cockp6zr3KGPgC",
    "ce_dm_mng": "🔗 كل ما يخص مادة الإدارة الهندسية وضبط الجودة:\nhttps://drive.google.com/drive/folders/1CnhE5_nTugvMnTGc3b61NPZ8JLwN_cIx",
    "ce_dm_struc1": "🔗 كل ما يخص مادة تحليل إنشاءات 1:\nhttps://drive.google.com/drive/folders/1j6um544BSHP0g-iePoxlLaUiMwNC3HOw",
    "ce_dm_struc2": "🔗 كل ما يخص مادة تحليل إنشاءات 2:\nhttps://drive.google.com/drive/folders/1F7yclgmoqsaX5RiCV3p3P-Y4J8AddTv1",

    # هندسة الميكانيك – إجباري تخصص
    "me_dm_cir1": "🔗 كل ما يخص مادة دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1zWr2kk4jznsqB2_VyDwUrlXAomX2ppJy",
    "me_dm_lab_cir1": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1LOn0kXufvISSPDu3X7BiMSY3u5xnppWh?hl=ar",
    "me_dm_cir2": "🔗 كل ما يخص مادة دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/11zw1ss3cgU3fX5xE3pd1bMAthrvUsasa",
    "me_dm_lab_cir2": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/1exrz303ktSkMn26VpbyR-dwwBH0MlEiL?hl=ar",
    "me_dm_con1": "🔗 كل ما يخص مادة أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar",
    "me_dm_lab_con1": "🔗 كل ما يخص مادة مختبر أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1iJuSOKY6c1LQ8oZ15ncKiaVxEOGlCHst?hl=ar",
    "me_dm_em": "🔗 كل ما يخص مادة آلات كهربائية:\nhttps://drive.google.com/drive/folders/11ONeQvvYjDBrCwFFbx7aiyu3U3GsbUDS",
    "me_dm_lab_em": "🔗 كل ما يخص مادة مختبر آلات كهربائية:\nhttps://drive.google.com/drive/folders/15bT6mBmbcNJuobmUny9ZhELwS3cZhLgr?hl=ar",
    "me_dm_elec": "🔗 كل ما يخص مادة إلكترونيات:\nhttps://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb",
    "me_dm_lab_elec": "🔗 كل ما يخص مادة مختبر إلكترونيات:\nhttps://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar",
    "me_dm_dig": "🔗 كل ما يخص مادة تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI",
    "me_dm_lab_dig": "🔗 كل ما يخص مادة مختبر تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar",
    "me_dm_pe": "🔗 كل ما يخص مادة إلكترونيات القدرة:\nhttps://drive.google.com/drive/folders/1JGMx_EgOqtappXrCG8DRPhyjsqPsAS6k",
    "me_dm_lab_pe": "🔗 كل ما يخص مادة مختبر إلكترونيات القدرة:\nhttps://drive.google.com/drive/folders/1DWK1Q6nvE4cLGul2ZhvM5AyJsTP4FVEb?hl=ar",
    "me_dm_thrm1": "🔗 كل ما يخص مادة الديناميكا الحرارية:\nhttps://drive.google.com/drive/folders/1bN_YHgvFio7VvALWn8bXUa1_tnReiY9T?hl=ar",
    "me_dm_thrm2": "🔗 كل ما يخص مادة ديناميكا حرارية (2):\nhttps://drive.google.com/drive/folders/1GWqkFlf3Lmp1MkhnhhUyG-2DdBBwtza4",
    "me_dm_fem": "🔗 كل ما يخص مادة طرق التحليل بالعناصر المحددة:\nhttps://drive.google.com/drive/folders/1AALjvwYQ8oaNTGzzKcA8HqxC-OpkpMc7",
    "me_dm_md2": "🔗 كل ما يخص مادة تصميم عناصر الآلات (2):\nhttps://drive.google.com/drive/folders/1nHuXfMbq2DLREUD5YDoyU3uXf6TQCKOK",
    "me_dm_sim": "🔗 كل ما يخص مادة تصميم أنظمة المحاكاة:\nhttps://drive.google.com/drive/folders/15R8KhaTnuJvIxShKql4y3cugxlVAV_qI",
    "me_dm_micro": "🔗 كل ما يخص مادة متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/15jlZjQKiTjJgMLO28f_h4u79IE5XYisr",
    "me_dm_lab_micro": "🔗 كل ما يخص مادة مختبر متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/1vdD5m2AxEr5W3QtIWu42SBdPf95wUND_?hl=ar",
    "me_dm_sig": "🔗 كل ما يخص مادة الإشارات والنظم:\nhttps://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0",
    "me_dm_plc": "🔗 كل ما يخص مادة أنظمة التحكم المبرمجة:\nhttps://drive.google.com/drive/folders/1-B9zlKvs7IebRZEungMNrQu6miLn0TS5",
    "me_dm_lab_plc": "🔗 كل ما يخص مادة مختبر أنظمة التحكم المبرمجة:\nhttps://drive.google.com/drive/folders/1XP4V02TjXmAtu2OPYnJ7lEOWC46-p655?hl=ar",
    "me_dm_eps1": "🔗 كل ما يخص مادة أنظمة قوى كهربائية 1:\nhttps://drive.google.com/drive/folders/11WaMIJF3MDdstrZkSidC_IzXjyl5ckqz",
    "me_dm_stat": "🔗 كل ما يخص مادة استاتيكا:\nhttps://drive.google.com/drive/folders/1of0sj2JlxoN66lyYtOngQqWSAyOgz512?hl=ar",
    "me_dm_lab_fluid": "🔗 كل ما يخص مادة مختبر ميكانيكا الموائع ونقل الحرارة:\nhttps://drive.google.com/drive/folders/1mNBVBQ2PJphdASfDnOAoKDxv7fSjl8vu",
    "me_dm_dyn": "🔗 كل ما يخص مادة ديناميكا:\nhttps://drive.google.com/drive/folders/1-MNDwo-cRXMKSI9_ROGBD7SKPM6NVAP_?hl=ar",
    "me_dm_ht": "🔗 كل ما يخص مادة الانتقال الحراري وميكانيكا الموائع:\nhttps://drive.google.com/drive/folders/1bakFrIO5JDa-B2cmKoPAD3KrEwtb51Km",
    "me_dm_cpp": "🔗 كل ما يخص مادة برمجة الحاسوب:\nhttps://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar",
    "me_dm_str": "🔗 كل ما يخص مادة قوة المواد:\nhttps://drive.google.com/drive/folders/12XA-itWG7wu9J4NOknCuZOvr4MErFmP6?hl=ar",
    "me_dm_lab_str": "🔗 كل ما يخص مادة مختبر قوة المواد:\nhttps://drive.google.com/drive/folders/1PkT0nYMxy9VHOl56edAg61bInofLPZjJ?hl=ar",
    "me_dm_mach": "🔗 كل ما يخص مادة نظرية الآلات:\nhttps://drive.google.com/drive/folders/1wHhv1cIbZgYZb5dFVVOghvqld3U-ThvI?hl=ar",
    "me_dm_md": "🔗 كل ما يخص مادة تصميم عناصر الآلات:\nhttps://drive.google.com/drive/folders/1C_aonz113miO6AGZSrmvPY8TdtOuXCeY?hl=ar",
    "me_dm_mat": "🔗 كل ما يخص مادة تطبيقات هندسية باستخدام MATLAB:\nhttps://drive.google.com/drive/folders/1hUfbichKsMgM_hNG4C1LE5Z_BvDIXHOw?hl=ar",
    "me_dm_vib": "🔗 كل ما يخص مادة اهتزازات ميكانيكية:\nhttps://drive.google.com/drive/folders/1C0om_juC5ywH095nHkePKzF3lbcMUBfl?hl=ar",
    "me_dm_con2": "🔗 كل ما يخص مادة أنظمة التحكم 2:\nhttps://drive.google.com/drive/folders/1Oles6Pz1htv4YMXp84d5K7adtj_tYP0m?hl=ar",
    "me_dm_mechd": "🔗 كل ما يخص مادة تصميم أنظمة الميكاترونيكس:\nhttps://drive.google.com/drive/folders/1fSO_OATeTpu3UMFRD_vElFaKnOahdZvF?hl=ar",
    "me_dm_rob": "🔗 كل ما يخص مادة الريبوتات:\nhttps://drive.google.com/drive/folders/1xK1hqQs9vsDM7jbOrijhdHLJXk-IE9_2?hl=ar",
    "me_dm_fluid": "🔗 كل ما يخص مادة ميكانيكا الموائع:\nhttps://drive.google.com/drive/folders/1bakFrIO5JDa-B2cmKoPAD3KrEwtb51Km?hl=ar",
    "me_dm_lab_fluid2": "🔗 كل ما يخص مادة مختبر ميكانيكا الموائع:\nhttps://drive.google.com/drive/folders/1mNBVBQ2PJphdASfDnOAoKDxv7fSjl8vu?hl=ar",
    "me_dm_cir": "🔗 كل ما يخص مادة دوائر كهربائية:\nhttps://drive.google.com/drive/folders/1Y4BPIHpd21iBm_9wSfDYPcyLFbBeU_kb",
    "me_dm_lab_cir": "🔗 كل ما يخص مادة مختبر دوائر كهربائية:\nhttps://drive.google.com/drive/folders/1oh7bNZxJtEows95EjCNRawxlfZ8SzZ8U?hl=ar",
    "me_dm_sen": "🔗 كل ما يخص مادة المجسات ومحولات الطاقة:\nhttps://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm",
    "me_dm_num": "🔗 كل ما يخص مادة تحليل عددي:\nhttps://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj",
    "me_dm_ic": "🔗 كل ما يخص مادة محرك الاحتراق الداخلي:\nhttps://drive.google.com/drive/folders/1Y0MooV0syFRLXKRITA0aGHSUPXtvEfYp?hl=ar",
    "me_dm_ac": "🔗 كل ما يخص مادة تكييف وتبريد:\nhttps://drive.google.com/drive/folders/1DE2IC8WXxwLLtc709sw-l7X5WX6Y8CUn",
    "me_dm_hyd": "🔗 كل ما يخص مادة أنظمة التحكم الهيدرولوكية والهوائية:\nhttps://drive.google.com/drive/folders/1CSKv_iJD7-W6kyIHRIwI9eWWYghwwSyO?hl=ar",
    "me_dm_meas": "🔗 كل ما يخص مادة قياسات كهربائية:\nhttps://drive.google.com/drive/folders/186kPiZPVbMlLaZ0nwvyWyfQY5NkDpXo3",
    "me_dm_lab_meas": "🔗 كل ما يخص مادة مختبر قياسات كهربائية:\nhttps://drive.google.com/drive/folders/17_RThMAo8ae6wsxj3ipgA9EP7Bbgm13j?hl=ar",
    "me_dm_auto_elec": "🔗 كل ما يخص مادة إلكترونيات وكهرباء السيارات:\nhttps://drive.google.com/drive/folders/1Ce-4LEeRYkrkMWQQqLeFZKdAAXD0y52Q?hl=ar",
    "me_dm_veh": "🔗 كل ما يخص مادة أنظمة المركبات:\nhttps://drive.google.com/drive/folders/1Mnx-_8RpYndH5kmGxfAiQCzMH6uEoLD0",
    "me_dm_veh_dyn": "🔗 كل ما يخص مادة ديناميكا واهتزازت المركبات:\nhttps://drive.google.com/drive/folders/1K8QD7U9duW_VY1XS9YxPjBucSPLqAYLd?hl=ar",
    "me_dm_lab_veh_dyn": "🔗 كل ما يخص مادة مختبر ديناميكا واهتزازت المركبات:\nhttps://drive.google.com/drive/folders/1MfkQKhqoOTekK-MZNhhZIZtvezQAB5UY",
    "me_dm_inst": "🔗 كل ما يخص مادة التمديدات الكهربائية:\nhttps://drive.google.com/drive/folders/1SdD9ZuTLwI-z25vYy5VWm4SFbpywVW0A",
    "me_dm_lab_inst": "🔗 كل ما يخص مادة مختبر التمديدات الكهربائية:\nhttps://drive.google.com/drive/folders/1XLJzjKQ5vJqdgB_R4y33exik-xyLMGsQ?hl=ar",
    "me_dm_saf": "🔗 كل ما يخص مادة هندسة السلامة:\nhttps://drive.google.com/drive/folders/1l0ORYZhMVxUJyQTHce47aAnSlPwLvEvQ?hl=ar",
    "me_dm_car2": "🔗 كل ما يخص مادة مشغل سيارات 2:\nhttps://drive.google.com/drive/folders/11tfyUh-4zC4zDQWPvYVsLVnFkyPS5xna?hl=ar",

    # هندسة الكهرباء – إجباري تخصص
    "ee_dm_ec1": "🔗 كل ما يخص مادة دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1zWr2kk4jznsqB2_VyDwUrlXAomX2ppJy",
    "ee_dm_lc1": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1LOn0kXufvISSPDu3X7BiMSY3u5xnppWh",
    "ee_dm_ec2": "🔗 كل ما يخص مادة دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/11zw1ss3cgU3fX5xE3pd1bMAthrvUsasa",
    "ee_dm_lc2": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/1exrz303ktSkMn26VpbyR-dwwBH0MlEiL",
    "ee_dm_cn1": "🔗 كل ما يخص مادة أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F",
    "ee_dm_ln1": "🔗 كل ما يخص مادة مختبر أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1iJuSOKY6c1LQ8oZ15ncKiaVxEOGlCHst",
    "ee_dm_lec": "🔗 كل ما يخص مادة مختبر دوائر كهربائية:\nhttps://drive.google.com/drive/folders/1oh7bNZxJtEows95EjCNRawxlfZ8SzZ8U",
    "ee_dm_el1": "🔗 كل ما يخص مادة إلكترونيات 1:\nhttps://drive.google.com/drive/folders/1h94fbWvDZFPposGGpAUkfU0cNDVUN9jt",
    "ee_dm_ll1": "🔗 كل ما يخص مادة مختبر إلكترونيات 1:\nhttps://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn",
    "ee_dm_el2": "🔗 كل ما يخص مادة إلكترونيات 2:\nhttps://drive.google.com/drive/folders/12OecrqIQHpLo7TWKtbLwyFyQM1r0Jllh",
    "ee_dm_dld": "🔗 كل ما يخص مادة تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI",
    "ee_dm_ldd": "🔗 كل ما يخص مادة مختبر تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ",
    "ee_dm_pe": "🔗 كل ما يخص مادة إلكترونيات القدرة:\nhttps://drive.google.com/drive/folders/1JGMx_EgOqtappXrCG8DRPhyjsqPsAS6k",
    "ee_dm_lpe": "🔗 كل ما يخص مادة مختبر إلكترونيات القدرة:\nhttps://drive.google.com/drive/folders/1DWK1Q6nvE4cLGul2ZhvM5AyJsTP4FVEb",
    "ee_dm_em": "🔗 كل ما يخص مادة كهرومغناطيسية:\nhttps://drive.google.com/drive/folders/11EZrizxPcbYY3xjGseDeOLLdFsIEunvM",
    "ee_dm_hv": "🔗 كل ما يخص مادة خطوط نقل الضغط العالي:\nhttps://drive.google.com/drive/folders/1MfeVA8i88yBAZJPKBZWHdev122IEElhJ",
    "ee_dm_sig": "🔗 كل ما يخص مادة الإشارات والنظم:\nhttps://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0",
    "ee_dm_com": "🔗 كل ما يخص مادة أنظمة الاتصالات:\nhttps://drive.google.com/drive/folders/12ZENHtxlaqjpYgV79NTBgDiNBqIqcfsn",
    "ee_dm_lco": "🔗 كل ما يخص مادة مختبر أنظمة الاتصالات:\nhttps://drive.google.com/drive/folders/1ysCfKkb8Pa-4DbvpVlu386-21TwIUEXr",
    "ee_dm_prb": "🔗 كل ما يخص مادة الاحتمالات والمتغيرات العشوائية:\nhttps://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV",
    "ee_dm_plc": "🔗 كل ما يخص مادة أنظمة التحكم المبرمجة:\nhttps://drive.google.com/drive/folders/1-B9zlKvs7IebRZEungMNrQu6miLn0TS5",
    "ee_dm_lpc": "🔗 كل ما يخص مادة مختبر أنظمة التحكم المبرمجة:\nhttps://drive.google.com/drive/folders/1XP4V02TjXmAtu2OPYnJ7lEOWC46-p655",
    "ee_dm_ep1": "🔗 كل ما يخص مادة أنظمة قوى كهربائية 1:\nhttps://drive.google.com/drive/folders/11WaMIJF3MDdstrZkSidC_IzXjyl5ckqz",
    "ee_dm_em1": "🔗 كل ما يخص مادة آلات كهربائية 1:\nhttps://drive.google.com/drive/folders/1-4IGpxohCaNpNa5UYyMiOrF3Lek7pjSC",
    "ee_dm_mic": "🔗 كل ما يخص مادة متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/15jlZjQKiTjJgMLO28f_h4u79IE5XYisr",
    "ee_dm_lmi": "🔗 كل ما يخص مادة مختبر متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/1vdD5m2AxEr5W3QtIWu42SBdPf95wUND_",
    "ee_dm_sd": "🔗 كل ما يخص مادة استاتيكا وديناميكا:\nhttps://drive.google.com/drive/folders/1xnChAL5DNph8HmQO-VNCnsYLDYLNV1kI",
    "ee_dm_mea": "🔗 كل ما يخص مادة قياسات كهربائية:\nhttps://drive.google.com/drive/folders/186kPiZPVbMlLaZ0nwvyWyfQY5NkDpXo3",
    "ee_dm_lme": "🔗 كل ما يخص مادة مختبر قياسات كهربائية:\nhttps://drive.google.com/drive/folders/17_RThMAo8ae6wsxj3ipgA9EP7Bbgm13j",
    "ee_dm_prg": "🔗 كل ما يخص مادة برمجة الحاسوب:\nhttps://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY",
    "ee_dm_ep2": "🔗 كل ما يخص مادة أنظمة قوى كهربائية 2:\nhttps://drive.google.com/drive/folders/1-03rv3TLoqVkAKfXnZPBfsMWMGU4lgtP",
    "ee_dm_dcd": "🔗 كل ما يخص مادة قيادة محركات التيار المستمر:\nhttps://drive.google.com/drive/folders/15w_AciZLn7_70NyMI3pB0y4474CizpWs",
    "ee_dm_acd": "🔗 كل ما يخص مادة قيادة محركات التيار المتردد:\nhttps://drive.google.com/drive/folders/1i6ME3YlM62Bgz0o8iNJhkSUBahNOY8zI",
    "ee_dm_em2": "🔗 كل ما يخص مادة آلات كهربائية 2:\nhttps://drive.google.com/drive/folders/1-7xQIuii6K_LeUI8-oXoV3jnlhmWhren",
    "ee_dm_lem": "🔗 كل ما يخص مادة مختبر آلات كهربائية:\nhttps://drive.google.com/drive/folders/15bT6mBmbcNJuobmUny9ZhELwS3cZhLgr",
    "ee_dm_ins": "🔗 كل ما يخص مادة التمديدات الكهربائية:\nhttps://drive.google.com/drive/folders/1SdD9ZuTLwI-z25vYy5VWm4SFbpywVW0A",
    "ee_dm_lin": "🔗 كل ما يخص مادة مختبر التمديدات الكهربائية:\nhttps://drive.google.com/drive/folders/1XLJzjKQ5vJqdgB_R4y33exik-xyLMGsQ",
    "ee_dm_st1": "🔗 كل ما يخص مادة تكنولوجيا الطاقة المستدامة 1:\nhttps://drive.google.com/drive/folders/1-1JedAsjr-R-4zxXVIjNJcLYDQa7-IfU",
    "ee_dm_hyd": "🔗 كل ما يخص مادة أنظمة التحكم الهيدروليكية:\nhttps://drive.google.com/drive/folders/1CSKv_iJD7-W6kyIHRIwI9eWWYghwwSyO",
    "ee_dm_st2": "🔗 كل ما يخص مادة تكنولوجيا الطاقة المستدامة 2:\nhttps://drive.google.com/drive/folders/1-1wBRd6PlW9G0Bh-_Z8sr44CDdCappYh",
    "ee_dm_ls2": "🔗 كل ما يخص مادة مختبر تكنولوجيا الطاقة المستدامة 2:\nhttps://drive.google.com/drive/folders/1hbpFRR5bXrOXPugYWqGfdwxEMU7Q-QUc",
    "ee_dm_ppe": "🔗 كل ما يخص مادة هندسة محطات التوليد:\nhttps://drive.google.com/drive/folders/1M6PrnSB542x8n2E-pkGbPBbfRZTGrhT4",
    "ee_dm_ele": "🔗 كل ما يخص مادة إلكترونيات:\nhttps://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb",
    "ee_dm_lel": "🔗 كل ما يخص مادة مختبر إلكترونيات:\nhttps://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn",
    "ee_dm_num": "🔗 كل ما يخص مادة تحليل عددي:\nhttps://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj",
    "ee_dm_sca": "🔗 كل ما يخص مادة أنظمة الإشراف:\nhttps://drive.google.com/drive/folders/1DBapVYC9KQGxuT3q0gNzd7c9fnCPUjZl",
    "ee_dm_thm": "🔗 كل ما يخص مادة الديناميكا الحرارية:\nhttps://drive.google.com/drive/folders/1bN_YHgvFio7VvALWn8bXUa1_tnReiY9T",
    "ee_dm_sen": "🔗 كل ما يخص مادة المجسات ومحولات الطاقة:\nhttps://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm",

    # هندسة الاتصالات – إجباري تخصص
    "te_dm_mic": "🔗 كل ما يخص مادة متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/15jlZjQKiTjJgMLO28f_h4u79IE5XYisr",
    "te_dm_mcl": "🔗 كل ما يخص مادة مختبر متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/1vdD5m2AxEr5W3QtIWu42SBdPf95wUND_?hl=ar",
    "te_dm_dld": "🔗 كل ما يخص مادة تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI",
    "te_dm_dll": "🔗 كل ما يخص مادة مختبر تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar",
    "te_dm_ele": "🔗 كل ما يخص مادة إلكترونيات:\nhttps://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb",
    "te_dm_lel": "🔗 كل ما يخص مادة مختبر إلكترونيات:\nhttps://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar",
    "te_dm_ctl": "🔗 كل ما يخص مادة أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar",
    "te_dm_lcl": "🔗 كل ما يخص مادة مختبر أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1iJuSOKY6c1LQ8oZ15ncKiaVxEOGlCHst?hl=ar",
    "te_dm_ec1": "🔗 كل ما يخص مادة دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1zWr2kk4jznsqB2_VyDwUrlXAomX2ppJy",
    "te_dm_lec": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1LOn0kXufvISSPDu3X7BiMSY3u5xnppWh?hl=ar",
    "te_dm_ec2": "🔗 كل ما يخص مادة دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/11zw1ss3cgU3fX5xE3pd1bMAthrvUsasa",
    "te_dm_lc2": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/1exrz303ktSkMn26VpbyR-dwwBH0MlEiL?hl=ar",
    "te_dm_dcm": "🔗 كل ما يخص مادة اتصالات رقمية:\nhttps://drive.google.com/drive/folders/1CCcNu0Y_DWD9lNSorrqAMnO6wfsNgWHV",
    "te_dm_prb": "🔗 كل ما يخص مادة الاحتمالات والمتغيرات العشوائية:\nhttps://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV",
    "te_dm_acm": "🔗 كل ما يخص مادة اتصالات تماثلية:\nhttps://drive.google.com/drive/folders/1ZCQDftVAUNN6pufMmFz2MniZkK2OJvTp",
    "te_dm_sig": "🔗 كل ما يخص مادة الإشارات والنظم:\nhttps://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0",
    "te_dm_emg": "🔗 كل ما يخص مادة كهرومغناطيسية:\nhttps://drive.google.com/drive/folders/11EZrizxPcbYY3xjGseDeOLLdFsIEunvM",
    "te_dm_aec": "🔗 كل ما يخص مادة إلكترونيات متقدمة للاتصالات:\nhttps://drive.google.com/drive/folders/1SOL5I1Im3twNrfKieLj0Kc4TWB30jowj",
    "te_dm_net": "🔗 كل ما يخص مادة شبكات حاسوب:\nhttps://drive.google.com/drive/folders/11xXsav473CKMGf36TZdIOj39StalkIAt",
    "te_dm_prg": "🔗 كل ما يخص مادة برمجة حاسوب:\nhttps://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar",
    "te_dm_aew": "🔗 كل ما يخص مادة الصوتيات والأمواج الكهرومغناطيسية:\nhttps://drive.google.com/drive/folders/1v7AWzoyTWJ5CADo-68oNMtp4hbXaCSfC",
    "te_dm_ofs": "🔗 كل ما يخص مادة أنظمة الألياف الضوئية:\nhttps://drive.google.com/drive/folders/13IlmE6sMct-gAdZxoTmhlZJxNJGGBjXN",
    "te_dm_ant": "🔗 كل ما يخص مادة الهوائيات وانتشار الأمواج:\nhttps://drive.google.com/drive/folders/1zRh06odBIGSNOkxwZwa7ONJ5JiAa-KJC",
    "te_dm_spc": "🔗 كل ما يخص مادة المجسات ومحولات الطاقة:\nhttps://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm",
    "te_dm_num": "🔗 كل ما يخص مادة تحليل عددي:\nhttps://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj",


    # هندسة الحاسوب – إجباري تخصص
    "cse_dm_cpp": "🔗 كل ما يخص مادة برمجة الحاسوب:\nhttps://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar",
    "cse_dm_dslab": "🔗 كل ما يخص مادة مختبر تركيب البيانات:\nhttps://drive.google.com/drive/folders/1eMTzUX_1TvhkoWctA64IsHP7nokKtTVa?hl=ar",
    "cse_dm_dis": "🔗 كل ما يخص مادة تراكيب الحوسبة المتقطعة:\nhttps://drive.google.com/drive/folders/1r19VoO7Jn3th47Yvv02xqp_j_cRIANer?hl=ar",
    "cse_dm_alg": "🔗 كل ما يخص مادة الخوارزميات:\nhttps://drive.google.com/drive/folders/1HW8jr8rkYG1mCTu5Hw7V9bu6XrlMLj1K?hl=ar",
    "cse_dm_os": "🔗 كل ما يخص مادة نظم التشغيل:\nhttps://drive.google.com/drive/folders/1h5UMPn2E9PKEbApKMgr5gw6fcQD75ICX?hl=ar",
    "cse_dm_db": "🔗 كل ما يخص مادة أنظمة قواعد البيانات:\nhttps://drive.google.com/drive/folders/1As24z-MhrkxUgOQCTvxulg3ZscQL2X01?hl=ar",
    "cse_dm_dblab": "🔗 كل ما يخص مادة مختبر أنظمة قواعد البيانات:\nhttps://drive.google.com/drive/folders/1gC2wrrVNaC2pFtTehECBQTq1YbVJ4fTW?hl=ar",
    "cse_dm_net": "🔗 كل ما يخص مادة شبكات الحاسوب:\nhttps://drive.google.com/drive/folders/1bHhvXwaW1gp1CnDiNqOpK8iuytzc5H31?hl=ar",
    "cse_dm_netlab": "🔗 كل ما يخص مادة مختبر شبكات الحاسوب:\nhttps://drive.google.com/drive/folders/1y1D1FDgygSb0fZihJya49RzePjdp874u?hl=ar",
    "cse_dm_isad": "🔗 كل ما يخص مادة تحليل وتصميم أنظمة المعلومات:\nhttps://drive.google.com/drive/folders/1oLU6aQTdXa7ktuODLajyWRrvO1AowfiZ?hl=ar",
    "cse_dm_arc": "🔗 كل ما يخص مادة معمارية الحاسوب:\nhttps://drive.google.com/drive/folders/1Ykp8VwEvfIgk0cJcLyZf6l8YY71fDftQ?hl=ar",
    "cse_dm_ass": "🔗 كل ما يخص مادة الأسمبلي:\nhttps://drive.google.com/drive/folders/1Mar8liqfh9GtAuJt_3HLhvy1F9df9iuF?hl=ar",
    "cse_dm_asslab": "🔗 كل ما يخص مادة مختبر الأسمبلي:\nhttps://drive.google.com/drive/folders/1Z8lWitiU9XDp5p8-fCKOvRklf4P0y7QT?hl=ar",
    "cse_dm_soft": "🔗 كل ما يخص مادة هندسة البرمجيات:\nhttps://drive.google.com/drive/folders/1I6Qon3_jvBG4KoGtmwQ1qBabzuA1ztvW?hl=ar",
    "cse_dm_netpro": "🔗 كل ما يخص مادة برمجة الشبكات:\nhttps://drive.google.com/drive/folders/1KGn9YDVnoZZVDPjfYa516ToWJHQZJmKm?hl=ar",
    "cse_dm_vhdl": "🔗 كل ما يخص مادة التصميم المنطقي عالي المستوى:\nhttps://drive.google.com/drive/folders/1cQhqZuOg05wOhLBfJCDErHo5Sdh9GWaD?hl=ar",
    "cse_dm_web": "🔗 كل ما يخص مادة تقنيات الانترنت وتطبيقات الويب:\nhttps://drive.google.com/drive/folders/1wz3InGxK3ZkUzeKVgACEB7k_lAP8Fyaa?hl=ar",
    "cse_dm_ai": "🔗 كل ما يخص مادة الذكاء الاصطناعي:\nhttps://drive.google.com/drive/folders/1EGiAnJdtjmYP6q5WxbvOzz4rd0O6nf0I?hl=ar",
    "cse_dm_cir": "🔗 كل ما يخص مادة الدوائر الكهربائية:\nhttps://drive.google.com/drive/folders/1Y4BPIHpd21iBm_9wSfDYPcyLFbBeU_kb",
    "cse_dm_cirlab": "🔗 كل ما يخص مادة مختبر الدوائر الكهربائية:\nhttps://drive.google.com/drive/folders/1oh7bNZxJtEows95EjCNRawxlfZ8SzZ8U?hl=ar",
    "cse_dm_ele": "🔗 كل ما يخص مادة الإلكترونيات:\nhttps://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb",
    "cse_dm_elelab": "🔗 كل ما يخص مادة مختبر الإلكترونيات:\nhttps://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar",
    "cse_dm_dig": "🔗 كل ما يخص مادة تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI",
    "cse_dm_diglab": "🔗 كل ما يخص مادة مختبر تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar",
    "cse_dm_dige": "🔗 كل ما يخص مادة إلكترونيات رقمية:\nhttps://drive.google.com/drive/folders/10BaqCIeCxxGmZFtNf0iHjLp0PGnXM3xe",
    "cse_dm_sig": "🔗 كل ما يخص مادة الإشارات والنظم:\nhttps://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0",
    "cse_dm_pro": "🔗 كل ما يخص مادة الاحتمالات والمتغيرات العشوائية:\nhttps://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV",
    "cse_dm_cs": "🔗 كل ما يخص مادة أنظمة الاتصالات:\nhttps://drive.google.com/drive/folders/12ZENHtxlaqjpYgV79NTBgDiNBqIqcfsn",
    "cse_dm_dsp": "🔗 كل ما يخص مادة معالجة الإشارات الرقمية:\nhttps://drive.google.com/drive/folders/1uXoNhnC_6O_Z-0EdQxZ4YUXNd1q74YUd",
    "cse_dm_con": "🔗 كل ما يخص مادة كنترول 1:\nhttps://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar",
    "cse_dm_num": "🔗 كل ما يخص مادة تحليل عددي:\nhttps://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj",

    # هندسة البناء – اختياري تخصص
    "ce_do_pave": "🔗 كل ما يخص مادة تصميم رصفات:\nhttps://drive.google.com/drive/folders/1fs_TN7ub9-ZdtNtLiagHLCxXThOBaZgd",
    "ce_do_resm": "🔗 كل ما يخص مادة مقدمة في منهجية البحث العلمي:\nhttps://drive.google.com/drive/folders/1ACRINqfCFGBZpLQGHtWUWyF5bVbC3Wj0?hl=ar",
    "ce_do_met2": "🔗 كل ما يخص مادة منشآت معدنية 2:\nhttps://drive.google.com/drive/folders/1GdvnmWUXeYUpzLBty0lqOJkUMJuVkSP6",
    "ce_do_conc3": "🔗 كل ما يخص مادة خرسانة 3:\nhttps://drive.google.com/drive/folders/1H7-AHGn7xrFhN2bIUoadzEr0aUD6VEq5",
    "ce_do_envimp": "🔗 كل ما يخص مادة تقييم الأثر البيئي:\nhttps://drive.google.com/drive/folders/10_qN-SPXs1LvtaabsBMGQAARc2h9wV8g",

    # هندسة الميكانيك – اختياري تخصص
    "me_do_dva": "🔗 كل ما يخص مادة ديناميكا واهتزازات المركبات:\nhttps://drive.google.com/drive/folders/1K8QD7U9duW_VY1XS9YxPjBucSPLqAYLd?hl=ar",
    "me_do_ldv": "🔗 كل ما يخص مادة مختبر ديناميكا واهتزازات المركبات:\nhttps://drive.google.com/drive/folders/1MfkQKhqoOTekK-MZNhhZIZtvezQAB5UY",
    "me_do_ss": "🔗 كل ما يخص مادة الإشارات والنظم:\nhttps://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0",
    "me_do_dsp": "🔗 كل ما يخص مادة معالجة الإشارات الرقمية DSP:\nhttps://drive.google.com/drive/folders/1uXoNhnC_6O_Z-0EdQxZ4YUXNd1q74YUd",
    "me_do_sen": "🔗 كل ما يخص مادة المجسات ومحولات الطاقة Sensors:\nhttps://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm",
    "me_do_ve": "🔗 كل ما يخص مادة إلكترونيات وكهرباء السيارات:\nhttps://drive.google.com/drive/folders/1Ce-4LEeRYkrkMWQQqLeFZKdAAXD0y52Q?hl=ar",

    # هندسة الكهرباء – اختياري تخصص
    "ee_do_adv": "🔗 كل ما يخص مادة إلكترونيات متقدمة:\nhttps://drive.google.com/drive/folders/1WJnZ2Jj9LmTrLo5alBkKXpHREBm9gwqc",
    "ee_do_pro": "🔗 كل ما يخص مادة أنظمة الحماية:\nhttps://drive.google.com/drive/folders/1tdQgHmwxD75frzSgs0gZL2i6Ev0ghKIR",
    "ee_do_dsp": "🔗 كل ما يخص مادة معالجة الإشارات الرقمية:\nhttps://drive.google.com/drive/folders/1uXoNhnC_6O_Z-0EdQxZ4YUXNd1q74YUd",
    "ee_do_ren": "🔗 كل ما يخص مادة تكنولوجيا الطاقة المتجددة:\nhttps://drive.google.com/drive/folders/1-2ojI_P9gWfSOm7UxKr3Y23s0qcdV4of",
    "ee_do_dig": "🔗 كل ما يخص مادة التحكم الرقمي:\nhttps://drive.google.com/drive/folders/1XnZmiJhFT-b8Y8EixQivQ9oA9hdhLyd3",
    "ee_do_net": "🔗 كل ما يخص مادة برمجة الشبكات:\nhttps://drive.google.com/drive/folders/1bHhvXwaW1gp1CnDiNqOpK8iuytzc5H31?hl=ar",
    "ee_do_ml": "🔗 كل ما يخص مادة تعلم الآلة:\nhttps://drive.google.com/drive/folders/1g5aWIGVzM-vkrCgH4XU7pi-vA3TcfuJG",
    "ee_do_cod": "🔗 كل ما يخص مادة نظرية المعلومات والترميز:\nhttps://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4",
    "ee_do_emw": "🔗 كل ما يخص مادة صوتيات وموجات كهرومغناطيسية:\nhttps://drive.google.com/drive/folders/1v7AWzoyTWJ5CADo-68oNMtp4hbXaCSfC",
    "ee_do_rob": "🔗 كل ما يخص مادة روبوتات:\nhttps://drive.google.com/drive/folders/1xK1hqQs9vsDM7jbOrijhdHLJXk-IE9_2?hl=ar",
    "ee_do_car": "🔗 كل ما يخص مادة إلكترونيات وكهرباء السيارات:\nhttps://drive.google.com/drive/folders/1Ce-4LEeRYkrkMWQQqLeFZKdAAXD0y52Q?hl=ar",

    # هندسة الاتصالات – اختياري تخصص
    "te_do_web": "🔗 كل ما يخص مادة تقنيات الانترنت وتطبيقات الويب:\nhttps://drive.google.com/drive/folders/1wz3InGxK3ZkUzeKVgACEB7k_lAP8Fyaa?hl=ar",
    "te_do_oop": "🔗 كل ما يخص مادة البرمجة الكينونية:\nhttps://drive.google.com/drive/folders/16mlcz7332pqsXWDcVM45Ez9Hi8KE2DWN?hl=ar",
    "te_do_db": "🔗 كل ما يخص مادة تركيب البيانات:\nhttps://drive.google.com/drive/folders/1MU9nY5LtI6_qzvvlIsM8p_JE9-OgYi7Z?hl=ar",
    "te_do_swe": "🔗 كل ما يخص مادة هندسة البرمجيات:\nhttps://drive.google.com/drive/folders/1I6Qon3_jvBG4KoGtmwQ1qBabzuA1ztvW?hl=ar",
    "te_do_cod": "🔗 كل ما يخص مادة نظرية المعلومات والترميز (كودينج):\nhttps://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4",

    # هندسة الحاسوب – اختياري تخصص
    "cse_do_adb": "🔗 كل ما يخص مادة مواضيع متقدمة في قواعد البيانات:\nhttps://drive.google.com/drive/folders/1yz8LMm1E4ErufxXHsA2ZBXw29cThH8wN?usp=drive_link",
    "cse_do_fib": "🔗 كل ما يخص مادة أنظمة الألياف الضوئية:\nhttps://drive.google.com/drive/folders/13IlmE6sMct-gAdZxoTmhlZJxNJGGBjXN",
    "cse_do_cs": "🔗 كل ما يخص مادة التشفير وأمن الشبكات:\nhttps://drive.google.com/drive/folders/11QMuiAHOtzktbKzEdXJkfpxf6h84neqt?hl=ar",
    "cse_do_acse": "🔗 كل ما يخص مادة مواضيع خاصة في هندسة أنظمة الحاسوب:\nhttps://drive.google.com/drive/folders/1yz8LMm1E4ErufxXHsA2ZBXw29cThH8wN?usp=drive_link",
    "cse_do_ml": "🔗 كل ما يخص مادة تعلم الآلة:\nhttps://drive.google.com/drive/folders/1r9W75-GeMHrNeNT7KXF-r_zqBM7QyoLp?hl=ar",
    "cse_do_dis": "🔗 كل ما يخص مادة أنماط التصميم:\nhttps://drive.google.com/drive/folders/1-KqrAUZeX7QYF4hHUqaDMnVMqLpFbx2k?hl=ar",
    "cse_do_dm": "🔗 كل ما يخص مادة تنجيم البيانات:\nhttps://drive.google.com/drive/folders/1yRaeasZdEedjtbgvAC2gY2c1JggQeAyL?hl=ar",
    "cse_do_cod": "🔗 كل ما يخص مادة نظرية المعلومات والترميز (كودينج):\nhttps://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4",
    "cse_do_sen": "🔗 كل ما يخص مادة المجسات ومحولات الطاقة (سنسور):\nhttps://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm",

    # إجباري الجامعة
    "shared_um_pi": "🔗 كل ما يخص مادة القضية الفلسطينية:\nhttps://drive.google.com/drive/folders/1AsOgF_Dqp2LKbKnfNjw12fTcEsx8-DI0",
    "shared_um_ar": "🔗 كل ما يخص مادة اللغة العربية:\nhttps://drive.google.com/drive/folders/16wiqvllo8uDoOt3mYA_tB_L8_DHmNG4F",
    "shared_um_cs": "🔗 كل ما يخص مادة مهارات الحاسوب:\nhttps://drive.google.com/drive/folders/1AqY3HGTmsEKJR-hUXoqR5-EeT-HE0HUe",
    "shared_um_com": "🔗 كل ما يخص مادة مهارات الاتصال:\nhttps://drive.google.com/drive/folders/1ag6esdUXaaFg8hKQRtdtTqjMIsPPLqxh",
    "shared_um_en": "🔗 كل ما يخص مادة اللغة الإنجليزية 1:\nhttps://drive.google.com/drive/folders/1QbSzV5flY50kuT1IrtFu-DhwZ4fc0dv7",
    "shared_um_is": "🔗 كل ما يخص مادة الدراسات الإسلامية:\nhttps://drive.google.com/drive/folders/1l_p-WrNOhr21VDdDE7FpNLy3QAbn1qg0",
    "shared_um_men": "🔗 كل ما يخص مادة استدراكي اللغة الإنجليزية:\nhttps://drive.google.com/drive/folders/1zoPLhWLfna2YHdZSQ5W2zMU9dDiiLq4I",

    # إجباري الكلية
    "shared_cm_chy1": "🔗 كل ما يخص مادة كيمياء عامة 1:\nhttps://drive.google.com/drive/folders/1_iO_Yk82kHH0bPz5I06lz1a8-2bt5o8N",
    "shared_cm_lin1": "🔗 كل ما يخص مادة رياضيات هندسية 1:\nhttps://drive.google.com/drive/folders/1p1uokT1-inoyoloh-AhYZ5GBmYiz1_UU",
    "shared_cm_lin2": "🔗 كل ما يخص مادة رياضيات هندسية 2:\nhttps://drive.google.com/drive/folders/16OqtFroWpAV0QgyVEIiIwrU0ICuoGoaj",
    "shared_cm_phy1": "🔗 كل ما يخص مادة فيزياء عامة 1:\nhttps://drive.google.com/drive/folders/1eTrvltnuqp8AHNQUS7JWffjC2ei9LAMM",
    "shared_cm_phy2": "🔗 كل ما يخص مادة فيزياء عامة 2:\nhttps://drive.google.com/drive/folders/1al3U6btk6IMrhDS-zC-uOYHkaF2YgkZ9",
    "shared_cm_cal1": "🔗 كل ما يخص مادة تفاضل وتكامل 1:\nhttps://drive.google.com/drive/folders/1FJFRsOX9isi5FpqIt3UhsceQZfxmZcQS",
    "shared_cm_cal2": "🔗 كل ما يخص مادة تفاضل وتكامل 2:\nhttps://drive.google.com/drive/folders/1JpqO5Pa7P0xk0D6C1auVNDCy_yqFnmgl",
    "shared_cm_phyl1": "🔗 كل ما يخص مادة مختبر فيزياء عامة 1:\nhttps://drive.google.com/drive/folders/1h_aqGgyD5V-IpG91KgUvCPec89FeSVtP?hl=ar",
    "shared_cm_phyl2": "🔗 كل ما يخص مادة مختبر فيزياء عامة 2:\nhttps://drive.google.com/drive/folders/1nO-MDLUo7-ihBxq-l-t2WG9au9ejWqWM?hl=ar",
    "shared_cm_ee": "🔗 كل ما يخص مادة اقتصاد هندسي:\nhttps://drive.google.com/drive/folders/1LiWsRZMwQH1LlKF513cy-umELAgankIO",
    "shared_cm_el": "🔗 كل ما يخص مادة مشغل هندسي:\nhttps://drive.google.com/drive/folders/1xYwCFikleDJloKnOG1jV5xtz4NSBMunG?hl=ar",
    "shared_cm_ed": "🔗 كل ما يخص مادة رسم هندسي:\nhttps://drive.google.com/drive/folders/19yDHfznncH4DuqWh5SlCy2siAZpNm7PV?hl=ar",
    "shared_cm_en2": "🔗 كل ما يخص مادة اللغة الإنجليزية 2:\nhttps://drive.google.com/drive/folders/1byU064ptdQ1mAxMSA8-twk8F5QZIp7Sy",
    "shared_cm_tw": "🔗 كل ما يخص مادة الكتابة التقنية وأخلاقيات المهنة:\nhttps://drive.google.com/drive/folders/1AjAp3qXHr4jEpCIuSlJktcAyX4pyPOK6?hl=ar",
    "shared_cm_sr": "🔗 كل ما يخص مادة مقدمة في منهجية البحث العلمي:\nhttps://drive.google.com/drive/folders/1ACRINqfCFGBZpLQGHtWUWyF5bVbC3Wj0?hl=ar",

    # اختياري الجامعة
    "shared_uo_spo": "🔗 كل ما يخص مادة الريادة والإبداع:\nhttps://drive.google.com/drive/folders/1BSYpLtfklUmW1UoimwokK-MZwGl99h4B",
    "shared_uo_aid": "🔗 كل ما يخص مادة إسعافات أولية:\nhttps://drive.google.com/drive/folders/1eMYmt_RpY6K-8xozQ83C3qtfc_iGLsLj",
    "shared_uo_hel": "🔗 كل ما يخص مادة الرياضة والصحة:\nhttps://drive.google.com/drive/folders/1_epsNMs45Pdqvk0AdWMaWLYtd0zZ9M5K",
    "shared_uo_isl": "🔗 كل ما يخص مادة الفكر الإسلامي:\nhttps://drive.google.com/drive/folders/1tfqMI736xu9bFpete1wxmNVE1jr1tTl7",
    "shared_uo_law": "🔗 كل ما يخص مادة القانون في حياتنا:\nhttps://drive.google.com/drive/folders/1_syfDYEHmtduIWok1u_jnkFBQ6WbqjV_",
    "shared_uo_chi": "🔗 كل ما يخص مادة تنشئة الأطفال:\nhttps://drive.google.com/drive/folders/1uQKcXDGt03A3Y_1c63nd7IUhfNZgUe0U",
    "shared_uo_civ": "🔗 كل ما يخص مادة حضارة إسلامية:\nhttps://drive.google.com/drive/folders/1z3q-13a_rOFO6dtZbMjAGwNEwCh2P1KV",
    "shared_uo_asp": "🔗 كل ما يخص مادة حركة أسيرة:\nhttps://drive.google.com/drive/folders/1-80OIWdDTtaapkyiURGmFpR4jLDg-UK_",
    "shared_uo_car": "🔗 كل ما يخص مادة مقدمة في هندسة السيارات:\nhttps://drive.google.com/drive/folders/1M6Ovliw7EJ9awE6Kg9oJuK4fG-EDTt5j",
    "shared_uo_iss": "🔗 كل ما يخص مادة قضايا معاصرة:\nhttps://drive.google.com/drive/folders/1-9b_H2IMbZLU3mg_aw1MpicFsCZsR6vw",
    "shared_uo_ant": "🔗 كل ما يخص مادة مكافحة الفساد:\nhttps://drive.google.com/drive/folders/1O-chfPMtuD-s2LBH9GW-H-x-qIYh6jBZ",
    "shared_uo_tur": "🔗 كل ما يخص مادة اللغة التركية:\nhttps://drive.google.com/drive/folders/1SgqSxvQruuFVIdOoYOw2tcDF3upC0jGC?hl=ar",
    "shared_uo_lib": "🔗 كل ما يخص مادة المكتبة وطرق البحث:\nhttps://drive.google.com/drive/folders/1X4AvmeV5CcQXvXmcsBqdmuiu_OK5WXOR",
    "shared_uo_heb": "🔗 كل ما يخص مادة اللغة العبرية:\nhttps://drive.google.com/drive/folders/1FuWbM2ZHMSsf4Gnp1TxeVA9mTzeoAZ5Q?hl=ar",
    "shared_uo_com": "🔗 كل ما يخص مادة مهارات التواصل المهني:\nhttps://drive.google.com/drive/folders/1ihs9BylIKUSQBIoRSWHxI18XTF2bbrmM?hl=ar",
    "shared_uo_jer": "🔗 كل ما يخص مادة تاريخ القدس:\nhttps://drive.google.com/drive/folders/1NMuX-KEWdye6nuYRTjb-qZk2aYwH0kwH?hl=ar",
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
        [InlineKeyboardButton("📚 مواد مشتركة", callback_data="shared_subjects")],
        [InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq")]
    ])


def specialization_menu(spec_code: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 إجباري تخصص", callback_data=f"{spec_code}_dm"), InlineKeyboardButton("📗 اختياري تخصص", callback_data=f"{spec_code}_do")],
        [InlineKeyboardButton("📚 مواد مشتركة", callback_data="shared_subjects")],
        [InlineKeyboardButton("Roadmaps", callback_data=f"{spec_code}_roadmaps"), InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ])



# def subjects_menu(spec_code: str):
#     return InlineKeyboardMarkup([
#         [InlineKeyboardButton("🔙 رجوع", callback_data=spec_code), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
#     ])

def shared_subjects_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 إجباري الجامعة", callback_data="shared_um")],
        [InlineKeyboardButton("📗 إجباري الكلية", callback_data="shared_cm")],
        [InlineKeyboardButton("📙 اختياري الجامعة", callback_data="shared_uo")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ])

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
        "تعليمات الاستخدام:\n"
        "/inst\n\n"
        "💡 لأي ملاحظات أو اقتراحات استخدم الأمر:\n"
        "/note\n\n"
        "عن الجمعية، وروابط خارجية:\n"
        "/about\n\n"
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

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "✳️ ما هي جمعية IVR\n\n"
        "⬅️ هي مؤسسة طلابية تطوعية غير ربحية مستقلة تقوم على تيسير أمور الطلبة في جامعة فلسطين التقنية (خضوري) ورفع مستواهم أكاديمياً ودينياً وثقافياً وعلمياً."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 موقع الجمعية", url="https://ivr-team-ptuk.github.io/IVR-Library/?fbclid=IwY2xjawNymGFleHRuA2FlbQIxMABicmlkETFMSGl6T3c4cVpQbWpuS2p5AR68bIpdoxosS9jmgwshDFGnri5PuCaE2fCbAJGlUuTNpUB3xavM77oyuWXnpA_aem_zRZUN5noXRofmBzQFgpyLQ")],
        [InlineKeyboardButton("🏛 منصة كلية الهندسة والتكنولوجيا IVR", url="https://www.facebook.com/groups/395354431026877/")],
        [
            InlineKeyboardButton("حساب الجمعية - فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100031851995367"),
            InlineKeyboardButton("حساب الجمعية - إنستغرام", url="https://www.instagram.com/ivr_ptuk/")
        ],
        [InlineKeyboardButton("اللجنة العلمية - فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100046123754881")],
        [
            InlineKeyboardButton("اللجنة الثقافية – فيسبوك", url="https://www.facebook.com/groups/395354431026877/user/100092553221922/"),
            InlineKeyboardButton("اللجنة الثقافية – إنستغرام", url="https://www.instagram.com/ivr.cultural/")
        ],
        [InlineKeyboardButton("▶️ قناة اليوتيوب", url="https://youtube.com/@ivr_channel?si=UPQeWn_mKz28jnZB")],
        # [InlineKeyboardButton("🤝 انضم لنا", url="PUT_LINK_HERE")],
        # [InlineKeyboardButton("📝 قدم مقترحاً", url="PUT_LINK_HERE")],
        [InlineKeyboardButton("🏫 IVR NAJAH", url="https://www.facebook.com/groups/2416874278576851/")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
    ])

    await update.message.reply_text(
        about_text,
        reply_markup=keyboard
    )

# async def bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "🤖 البوتات المرتبطة:\n"
#         "@tamfk2006\n"
#         "@Tak6Bot\n"
#         "@IVR_Library_bot"
#     )


# =========================
# Callback Buttons
# =========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ---- Main specializations ----

    if data == "shared_subjects":
        await query.edit_message_text(
            text="📚 المواد المشتركة بين جميع التخصصات:",
            reply_markup=shared_subjects_menu()
        )

    elif data =="shared_um":
        await query.edit_message_text(
            text="📚 إجباري الجامعة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("مهارات الحاسوب", callback_data=f"{data}_cs"), InlineKeyboardButton("مهارات الاتصال", callback_data=f"{data}_com")],
                [InlineKeyboardButton("اللغة العربية", callback_data=f"{data}_ar"), InlineKeyboardButton("اللغة الإنجليزية 1", callback_data=f"{data}_en")],
                [InlineKeyboardButton("الدراسات الإسلامية", callback_data=f"{data}_is"), InlineKeyboardButton("القضية الفلسطينية", callback_data=f"{data}_pi")],
                [InlineKeyboardButton("استدراكي اللغة الإنجليزية", callback_data=f"{data}_men")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data=="shared_cm":
        await query.edit_message_text(
            text="📚 إجباري الكلية:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رسم هندسي", callback_data=f"{data}_ed"),InlineKeyboardButton("مشغل هندسي", callback_data=f"{data}_el"), InlineKeyboardButton("اقتصاد هندسي", callback_data=f"{data}_ee")],
                [InlineKeyboardButton("الكتابة التقنية وأخلاقيات المهنة", callback_data=f"{data}_tw")],
                [InlineKeyboardButton("تفاضل وتكامل 1", callback_data=f"{data}_cal1"),InlineKeyboardButton("تفاضل وتكامل 2", callback_data=f"{data}_cal2")],
                [InlineKeyboardButton("رياضيات هندسية 1", callback_data=f"{data}_lin1"),InlineKeyboardButton("رياضيات هندسية 2", callback_data=f"{data}_lin2")],
                [InlineKeyboardButton("فيزياء عامة 1", callback_data=f"{data}_phy1"),InlineKeyboardButton("فيزياء عامة 2", callback_data=f"{data}_phy2")],
                [InlineKeyboardButton("مختبر فيزياء 1", callback_data=f"{data}_phyl1"),InlineKeyboardButton("مختبر فيزياء 2", callback_data=f"{data}_phyl2")],
                [InlineKeyboardButton("كيمياء عامة 1", callback_data=f"{data}_chy1"),InlineKeyboardButton("اللغة الإنجليزية 2", callback_data=f"{data}_en2")],
                [InlineKeyboardButton("مقدمة في منهجية البحث العلمي", callback_data=f"{data}_sr")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data=="shared_uo":
        await query.edit_message_text(
            text="📚 اختياري الجامعة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("الريادة والابداع", callback_data=f"{data}_spo"), InlineKeyboardButton("إسعافات أولية", callback_data=f"{data}_aid")],
                [InlineKeyboardButton("الرياضة والصحة", callback_data=f"{data}_hel"), InlineKeyboardButton("الفكر الإسلامي", callback_data=f"{data}_isl")],
                [InlineKeyboardButton("القانون في حياتنا", callback_data=f"{data}_law"), InlineKeyboardButton("تنشئة الأطفال", callback_data=f"{data}_chi")],
                [InlineKeyboardButton("حضارة إسلامية", callback_data=f"{data}_civ"), InlineKeyboardButton("حركة أسيرة", callback_data=f"{data}_asp")],
                [InlineKeyboardButton("مقدمة في هندسة السيارات", callback_data=f"{data}_car"), InlineKeyboardButton("مهارات التواصل المهني", callback_data=f"{data}_com")],
                [InlineKeyboardButton("مكافحة الفساد", callback_data=f"{data}_ant"), InlineKeyboardButton("قضايا معاصرة", callback_data=f"{data}_iss")],
                [InlineKeyboardButton("اللغة التركية", callback_data=f"{data}_tur"), InlineKeyboardButton("المكتبة وطرق البحث", callback_data=f"{data}_lib")],
                [InlineKeyboardButton("اللغة العبرية", callback_data=f"{data}_heb"), InlineKeyboardButton("تاريخ القدس", callback_data=f"{data}_jer")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )


    elif data in ["cse", "me", "ee", "te", "ce"]:
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


    # # ---- Subjects ----
    # elif data.endswith("_subjects"):
    #     spec = data.replace("_subjects", "")
    #     await query.edit_message_text(
    #         text="      📘 اخـــــــتــــــر نـــــــوع الــــــمـــــواد:      ",
    #         reply_markup=subjects_menu(spec)
    #     )

    # ---- Subject lists (example implementation) ----
    elif data.endswith(("cse_dm")):
        await query.edit_message_text(
            text="حاسوب - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("برمجة الحاسوب", callback_data=f"{data}_cpp"), InlineKeyboardButton("البرمجة الكينونية", callback_data=f"{data}_java"), InlineKeyboardButton("تركيب البيانات", callback_data=f"{data}_ds")],
                [InlineKeyboardButton("م. تركيب البيانات", callback_data=f"{data}_dslab"), InlineKeyboardButton("تراكيب الحوسبة المتقطعة", callback_data=f"{data}_dis")], 
                [InlineKeyboardButton("نظم تشغيل", callback_data=f"{data}_os"), InlineKeyboardButton("خوارزميات", callback_data=f"{data}_alg"), InlineKeyboardButton("قواعد البيانات", callback_data=f"{data}_db")],
                [InlineKeyboardButton("شبكات الحاسوب", callback_data=f"{data}_net"), InlineKeyboardButton("م. قواعد البيانات", callback_data=f"{data}_dblab")],
                [InlineKeyboardButton("معمارية الحاسوب", callback_data=f"{data}_arc"), InlineKeyboardButton("م. شبكات الحاسوب", callback_data=f"{data}_netlab")],
                [InlineKeyboardButton("تحليل وتصميم أنظمة المعلومات", callback_data=f"{data}_isad")],
                [InlineKeyboardButton("م. أسمبلي", callback_data=f"{data}_asslab"), InlineKeyboardButton("أسمبلي", callback_data=f"{data}_ass"), InlineKeyboardButton("هندسة برمجيات", callback_data=f"{data}_soft")],
                [InlineKeyboardButton("التصميم المنطقي عالي المستوى", callback_data=f"{data}_vhdl")],
                [InlineKeyboardButton("تقنيات الانترنت وتطبيقات الويب", callback_data=f"{data}_web")],
                [InlineKeyboardButton("الذكاء الاصطناعي", callback_data=f"{data}_ai"), InlineKeyboardButton("برمجة الشبكات", callback_data=f"{data}_netpro")],
                [InlineKeyboardButton("الدوائر الكهربائية", callback_data=f"{data}_cir"), InlineKeyboardButton("م. الدوائر الكهربائية", callback_data=f"{data}_cirlab")],
                [InlineKeyboardButton("إلكترونيات", callback_data=f"{data}_ele"), InlineKeyboardButton("م. إلكترونيات", callback_data=f"{data}_elelab")],
                [InlineKeyboardButton("تصميم الدوائر المنطقية", callback_data=f"{data}_dig")],
                [InlineKeyboardButton("م. تصميم الدوائر المنطقية", callback_data=f"{data}_diglab")],
                [InlineKeyboardButton("إلكترونيات رقمية", callback_data=f"{data}_dige"), InlineKeyboardButton("الإشارات والنظم", callback_data=f"{data}_sig")],
                [InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", callback_data=f"{data}_pro")],
                [InlineKeyboardButton("أنظمة الاتصالات", callback_data=f"{data}_cs"), InlineKeyboardButton("معالجة الإشارات الرقمية", callback_data=f"{data}_dsp")],
                [InlineKeyboardButton("أنظمة التحكم 1", callback_data=f"{data}_con"), InlineKeyboardButton("تحليل عددي", callback_data=f"{data}_num")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="cse"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data.endswith(("cse_do")):
        await query.edit_message_text(
            text="حاسوب - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("مواضيع متقدمة في قواعد البيانات", callback_data=f"{data}_adb")],
                [InlineKeyboardButton("أنظمة الألياف الضوئية", callback_data=f"{data}_fib")],
                [InlineKeyboardButton("التشفير وأمن الشبكات", callback_data=f"{data}_cs"), InlineKeyboardButton("تنجيم البيانات", callback_data=f"{data}_dm")],
                [InlineKeyboardButton("مواضيع خاصة في هندسة انظمة الحاسوب", callback_data=f"{data}_acse")],
                [InlineKeyboardButton("تعلم الآلة", callback_data=f"{data}_ml"), InlineKeyboardButton("أنماط التصميم", callback_data=f"{data}_dis")],
                [InlineKeyboardButton("نظرية المعلومات والترميز (كودينج)", callback_data=f"{data}_cod")],
                [InlineKeyboardButton("المجسات ومحولات الطاقة (سنسور)", callback_data=f"{data}_sen")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="cse"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data.endswith(("te_dm")):
        await query.edit_message_text(
            text="اتصالات - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("م. متحكمات دقيقة", callback_data=f"{data}_mcl"), InlineKeyboardButton("متحكمات دقيقة", callback_data=f"{data}_mic")],
                [InlineKeyboardButton("م. تصميم الدوائر المنطقية", callback_data=f"{data}_dll"), InlineKeyboardButton("تصميم الدوائر المنطقية", callback_data=f"{data}_dld")],
                [InlineKeyboardButton("م. إلكترونيات", callback_data=f"{data}_lel"), InlineKeyboardButton("إلكترونيات", callback_data=f"{data}_ele")],
                [InlineKeyboardButton("م. أنظمة تحكم 1", callback_data=f"{data}_lcl"), InlineKeyboardButton("أنظمة تحكم 1", callback_data=f"{data}_ctl")],
                [InlineKeyboardButton("م. دوائر كهربائية 1", callback_data=f"{data}_lec"), InlineKeyboardButton("دوائر كهربائية 1", callback_data=f"{data}_ec1")],
                [InlineKeyboardButton("م. دوائر كهربائية 2", callback_data=f"{data}_lc2"), InlineKeyboardButton("دوائر كهربائية 2", callback_data=f"{data}_ec2")],
                [InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", callback_data=f"{data}_prb")],
                [InlineKeyboardButton("اتصالات تماثلية", callback_data=f"{data}_acm"), InlineKeyboardButton("اتصالات رقمية", callback_data=f"{data}_dcm")],
                [InlineKeyboardButton("كهرومغناطيسية", callback_data=f"{data}_emg"), InlineKeyboardButton("الإشارات والنظم", callback_data=f"{data}_sig")],
                [InlineKeyboardButton("إلكترونيات متقدمة للاتصالات", callback_data=f"{data}_aec")],
                [InlineKeyboardButton("برمجة حاسوب", callback_data=f"{data}_prg"), InlineKeyboardButton("شبكات حاسوب", callback_data=f"{data}_net")],
                [InlineKeyboardButton("الصوتيات والأمواج الكهرومغناطيسية", callback_data=f"{data}_aew")],
                [InlineKeyboardButton("الهوائيات وانتشار الأمواج", callback_data=f"{data}_ant")],
                [InlineKeyboardButton("المجسات ومحولات الطاقة", callback_data=f"{data}_spc")],
                [InlineKeyboardButton("تحليل عددي", callback_data=f"{data}_num"), InlineKeyboardButton("أنظمة الألياف الضوئية", callback_data=f"{data}_ofs")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="te"),
                     InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data.endswith(("te_do")):
        await query.edit_message_text(
            text="اتصالات - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("تقنيات الإنترنت وتطبيقات الويب", callback_data=f"{data}_web")],
                [InlineKeyboardButton("تركيب بيانات", callback_data=f"{data}_db"), InlineKeyboardButton("البرمجة الكينونية", callback_data=f"{data}_oop")],
                [InlineKeyboardButton("هندسة البرمجيات", callback_data=f"{data}_swe")],
                [InlineKeyboardButton("نظرية المعلومات والترميز (كودينج)", callback_data=f"{data}_cod")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="te"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data.endswith(("ee_dm")):
        await query.edit_message_text(
            text="كهرباء - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("م. دوائر كهربائية 1", callback_data=f"{data}_lc1"), InlineKeyboardButton("دوائر كهربائية 1", callback_data=f"{data}_ec1")],
                [InlineKeyboardButton("م. دوائر كهربائية 2", callback_data=f"{data}_lc2"), InlineKeyboardButton("دوائر كهربائية 2", callback_data=f"{data}_ec2")],
                [InlineKeyboardButton("م. أنظمة تحكم 1", callback_data=f"{data}_ln1"), InlineKeyboardButton("أنظمة تحكم 1", callback_data=f"{data}_cn1")],
                [InlineKeyboardButton("م. إلكترونيات 1", callback_data=f"{data}_ll1"), InlineKeyboardButton("إلكترونيات 1", callback_data=f"{data}_el1")],
                [InlineKeyboardButton("إلكترونيات 2", callback_data=f"{data}_el2")],
                [InlineKeyboardButton("م. تصميم دوائر المنطقية", callback_data=f"{data}_ldd"), InlineKeyboardButton("تصميم الدوائر المنطقية", callback_data=f"{data}_dld")],
                [InlineKeyboardButton("م. إلكترونيات القدرة", callback_data=f"{data}_lpe"), InlineKeyboardButton("إلكترونيات القدرة", callback_data=f"{data}_pe")],
                [InlineKeyboardButton("خطوط نقل الضغط العالي", callback_data=f"{data}_hv")],
                [InlineKeyboardButton("الإشارات والنظم", callback_data=f"{data}_sig"), InlineKeyboardButton("كهرومغناطيسية", callback_data=f"{data}_em")],
                [InlineKeyboardButton("م. أنظمة الاتصالات", callback_data=f"{data}_lco"), InlineKeyboardButton("أنظمة الاتصالات", callback_data=f"{data}_com")],
                [InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", callback_data=f"{data}_prb")],
                [InlineKeyboardButton("م. أنظمة التحكم المبرمجة", callback_data=f"{data}_lpc"), InlineKeyboardButton("أنظمة التحكم المبرمجة", callback_data=f"{data}_plc")],
                [InlineKeyboardButton("أنظمة قوى كهربائية 1", callback_data=f"{data}_ep1"), InlineKeyboardButton("آلات كهربائية 1", callback_data=f"{data}_em1")],
                [InlineKeyboardButton("م. متحكمات دقيقة", callback_data=f"{data}_lmi"), InlineKeyboardButton("متحكمات دقيقة", callback_data=f"{data}_mic")],
                [InlineKeyboardButton("استاتيكا وديناميكا", callback_data=f"{data}_sd"), InlineKeyboardButton("برمجة الحاسوب", callback_data=f"{data}_prg")],
                [InlineKeyboardButton("م. قياسات كهربائية", callback_data=f"{data}_lme"), InlineKeyboardButton("قياسات كهربائية", callback_data=f"{data}_mea")],
                [InlineKeyboardButton("أنظمة قوى كهربائية 2", callback_data=f"{data}_ep2")],
                [InlineKeyboardButton("قيادة محركات التيار المستمر", callback_data=f"{data}_dcd")],
                [InlineKeyboardButton("قيادة محركات التيار المتردد", callback_data=f"{data}_acd")],
                [InlineKeyboardButton("م. آلات كهربائية", callback_data=f"{data}_lem"), InlineKeyboardButton("آلات كهربائية 2", callback_data=f"{data}_em2")],
                [InlineKeyboardButton("م. التمديدات الكهربائية", callback_data=f"{data}_lin"), InlineKeyboardButton("التمديدات الكهربائية", callback_data=f"{data}_ins")],
                [InlineKeyboardButton("تكنولوجيا الطاقة المستدامة 1", callback_data=f"{data}_st1")],
                [InlineKeyboardButton("تكنولوجيا الطاقة المستدامة 2", callback_data=f"{data}_st2")],
                [InlineKeyboardButton("م. تكنولوجيا الطاقة المستدامة 2", callback_data=f"{data}_ls2")],
                [InlineKeyboardButton("هندسة محطات التوليد", callback_data=f"{data}_ppe"), InlineKeyboardButton("أنظمة التحكم الهيدروليكية", callback_data=f"{data}_hyd")],
                [InlineKeyboardButton("م. إلكترونيات", callback_data=f"{data}_lel"), InlineKeyboardButton("إلكترونيات", callback_data=f"{data}_ele")],
                [InlineKeyboardButton("أنظمة الإشراف", callback_data=f"{data}_sca"), InlineKeyboardButton("تحليل عددي", callback_data=f"{data}_num")],
                [InlineKeyboardButton("المجسات ومحولات الطاقة", callback_data=f"{data}_sen"), InlineKeyboardButton("الديناميكا الحرارية", callback_data=f"{data}_thm")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="ee"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data.endswith(("ee_do")):
        await query.edit_message_text(
            text="كهرباء - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("أنظمة الحماية", callback_data=f"{data}_pro"), InlineKeyboardButton("إلكترونيات متقدمة", callback_data=f"{data}_adv")],
                [InlineKeyboardButton("معالجة الإشارات الرقمية", callback_data=f"{data}_dsp")],
                [InlineKeyboardButton("تكنولوجيا الطاقة المتجددة", callback_data=f"{data}_ren")],
                [InlineKeyboardButton("برمجة الشبكات", callback_data=f"{data}_net"), InlineKeyboardButton("التحكم الرقمي", callback_data=f"{data}_dgc")],
                [InlineKeyboardButton("نظرية المعلومات والترميز(كودينج)", callback_data=f"{data}_cod")],
                [InlineKeyboardButton("صوتيات وموجات كهرومغناطيسية", callback_data=f"{data}_emw")],
                [InlineKeyboardButton("روبوتات", callback_data=f"{data}_rob"), InlineKeyboardButton("تعلم الآلة", callback_data=f"{data}_ml")],
                [InlineKeyboardButton("إلكترونيات وكهرباء السيارات", callback_data=f"{data}_car")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="ee"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data.endswith(("me_dm")):
        await query.edit_message_text(
            text="ميكانيك وميكاترونيكس - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("م. دوائر كهربائية 1", callback_data=f"{data}_lab_cir1"), InlineKeyboardButton("دوائر كهربائية 1", callback_data=f"{data}_cir1")],
                [InlineKeyboardButton("م. دوائر كهربائية 2", callback_data=f"{data}_lab_cir2"), InlineKeyboardButton("دوائر كهربائية 2", callback_data=f"{data}_cir2")],
                [InlineKeyboardButton("م. أنظمة تحكم 1", callback_data=f"{data}_lab_con1"), InlineKeyboardButton("أنظمة تحكم 1", callback_data=f"{data}_con1")],
                [InlineKeyboardButton("م. آلات كهربائية", callback_data=f"{data}_lab_em"), InlineKeyboardButton("آلات كهربائية", callback_data=f"{data}_em")],
                [InlineKeyboardButton("م. إلكترونيات", callback_data=f"{data}_lab_elec"),InlineKeyboardButton("إلكترونيات", callback_data=f"{data}_elec")],
                [InlineKeyboardButton("م.تصميم دوائر منطقية", callback_data=f"{data}_lab_dig"), InlineKeyboardButton("تصميم الدوائر المنطقية", callback_data=f"{data}_dig")],
                [InlineKeyboardButton("م. إلكترونيات القدرة", callback_data=f"{data}_lab_pe"), InlineKeyboardButton("إلكترونيات القدرة", callback_data=f"{data}_pe")],
                [InlineKeyboardButton("ديناميكا حرارية (2)", callback_data=f"{data}_thrm2"), InlineKeyboardButton("الديناميكا الحرارية", callback_data=f"{data}_thrm1")],
                [InlineKeyboardButton("طرق التحليل بالعناصر المحددة", callback_data=f"{data}_fem")],
                [InlineKeyboardButton("تصميم عناصر الآلات (2)", callback_data=f"{data}_md2")],
                [InlineKeyboardButton("تصميم أنظمة المحاكاة", callback_data=f"{data}_sim")],
                [InlineKeyboardButton("م. متحكمات دقيقة", callback_data=f"{data}_lab_micro"), InlineKeyboardButton("متحكمات دقيقة", callback_data=f"{data}_micro")],
                [InlineKeyboardButton("م. أنظمة التحكم المبرمجة", callback_data=f"{data}_lab_plc"), InlineKeyboardButton("أنظمة التحكم المبرمجة", callback_data=f"{data}_plc")],
                [InlineKeyboardButton("استاتيكا", callback_data=f"{data}_stat"), InlineKeyboardButton("الإشارات والنظم", callback_data=f"{data}_sig")],
                [InlineKeyboardButton("م. ميكانيكا الموائع ونقل الحرارة", callback_data=f"{data}_lab_fluid")],
                [InlineKeyboardButton("ديناميكا", callback_data=f"{data}_dyn"), InlineKeyboardButton("أنظمة قوى كهربائية 1", callback_data=f"{data}_eps1")],
                [InlineKeyboardButton("الانتقال الحراري وميكانيكا الموائع", callback_data=f"{data}_ht")],
                [InlineKeyboardButton("م. قوة المواد", callback_data=f"{data}_lab_str"), InlineKeyboardButton("قوة المواد", callback_data=f"{data}_str")],
                [InlineKeyboardButton("تصميم عناصر الآلات", callback_data=f"{data}_md"), InlineKeyboardButton("نظرية الآلات", callback_data=f"{data}_mach")],
                [InlineKeyboardButton("تطبيقات هندسية باستخدام MATLAB", callback_data=f"{data}_mat")],
                [InlineKeyboardButton("اهتزازات ميكانيكية", callback_data=f"{data}_vib"), InlineKeyboardButton("برمجة الحاسوب", callback_data=f"{data}_cpp")],
                [InlineKeyboardButton("تصميم أنظمة الميكاترونيكس", callback_data=f"{data}_mechd"), InlineKeyboardButton("أنظمة التحكم 2", callback_data=f"{data}_con2")],
                [InlineKeyboardButton("الروبوتات", callback_data=f"{data}_rob"), InlineKeyboardButton("المجسات ومحولات الطاقة", callback_data=f"{data}_sen")],
                [InlineKeyboardButton("م. ميكانيكا الموائع", callback_data=f"{data}_lab_fluid2"), InlineKeyboardButton("ميكانيكا الموائع", callback_data=f"{data}_fluid")],
                [InlineKeyboardButton("م. دوائر كهربائية", callback_data=f"{data}_lab_cir"), InlineKeyboardButton("دوائر كهربائية", callback_data=f"{data}_cir")],
                [InlineKeyboardButton("محرك الاحتراق الداخلي", callback_data=f"{data}_ic"), InlineKeyboardButton("تحليل عددي", callback_data=f"{data}_num")],
                [InlineKeyboardButton("أنظمة التحكم الهيدرولوكية والهوائية", callback_data=f"{data}_hyd")],
                [InlineKeyboardButton("م. قياسات كهربائية", callback_data=f"{data}_lab_meas"), InlineKeyboardButton("قياسات كهربائية", callback_data=f"{data}_meas")],
                [InlineKeyboardButton("إلكترونيات وكهرباء السيارات", callback_data=f"{data}_auto_elec")],
                [InlineKeyboardButton("أنظمة المركبات", callback_data=f"{data}_veh"), InlineKeyboardButton("تكييف وتبريد", callback_data=f"{data}_ac")],
                [InlineKeyboardButton("ديناميكا واهتزازت المركبات", callback_data=f"{data}_veh_dyn")],
                [InlineKeyboardButton("م. ديناميكا واهتزازت المركبات", callback_data=f"{data}_lab_veh_dyn")],
                [InlineKeyboardButton("م. التمديدات الكهربائية", callback_data=f"{data}_lab_inst"), InlineKeyboardButton("التمديدات الكهربائية", callback_data=f"{data}_inst")],
                [InlineKeyboardButton("مشغل سيارات 2", callback_data=f"{data}_car2"), InlineKeyboardButton("هندسة السلامة", callback_data=f"{data}_saf")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="me"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data.endswith(("me_do")):
        await query.edit_message_text(
            text="ميكانيك وميكاترونيكس - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ديناميكا واهتزازات المركبات", callback_data=f"{data}_dva")],
                [InlineKeyboardButton("مختبر ديناميكا واهتزازات المركبات", callback_data=f"{data}_ldv")],
                [InlineKeyboardButton("الإشارات والنظم", callback_data=f"{data}_ss")],
                [InlineKeyboardButton("معالجة الإشارات الرقمية DSP", callback_data=f"{data}_dsp")],
                [InlineKeyboardButton("المجسات ومحولات الطاقة Sensors", callback_data=f"{data}_sen")],
                [InlineKeyboardButton("إلكترونيات وكهرباء السيارات", callback_data=f"{data}_ve")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="me"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data.endswith(("ce_dm")):
        await query.edit_message_text(
            text="بناء ومدني - إجباري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", callback_data=f"{data}_prob")],
                [InlineKeyboardButton("برمجة الحاسوب", callback_data=f"{data}_prog"), InlineKeyboardButton("رسم هندسي", callback_data=f"{data}_draw")],
                [InlineKeyboardButton("ديناميكا", callback_data=f"{data}_dyn"), InlineKeyboardButton("استاتيكا", callback_data=f"{data}_stat")],
                [InlineKeyboardButton("الانتقال الحراري وميكانيكا الموائع", callback_data=f"{data}_heat")],
                [InlineKeyboardButton("مختبر قوة المواد", callback_data=f"{data}_labmat"), InlineKeyboardButton("قوة المواد", callback_data=f"{data}_matstr")],
                [InlineKeyboardButton("مختبر مساحة", callback_data=f"{data}_labsur"), InlineKeyboardButton("مساحة", callback_data=f"{data}_survey")],
                [InlineKeyboardButton("تكنولوجيا مواد البناء", callback_data=f"{data}_tech")],
                [InlineKeyboardButton("مختبر ميكانيكا التربة", callback_data=f"{data}_labsoil"), InlineKeyboardButton("ميكانيكا التربة", callback_data=f"{data}_soil")],
                [InlineKeyboardButton("خرسانة 2", callback_data=f"{data}_conc2"), InlineKeyboardButton("خرسانة 1", callback_data=f"{data}_conc1")],
                [InlineKeyboardButton("الإدارة المستدامة لمخلفات البيئة", callback_data=f"{data}_env")],
                [InlineKeyboardButton("تكنولوجيا الإنارة والتمديدات الكهربائية", callback_data=f"{data}_light")],
                [InlineKeyboardButton("تصميم رصفات", callback_data=f"{data}_pave"), InlineKeyboardButton("التدفئة والتكييف والتبريد", callback_data=f"{data}_hvac")],
                [InlineKeyboardButton("المباني صديقة البيئة", callback_data=f"{data}_green"), InlineKeyboardButton("هندسة أساسات", callback_data=f"{data}_found")],
                [InlineKeyboardButton("أنظمة توزيع المياه وأنظمة الصرف الصحي", callback_data=f"{data}_water")],
                [InlineKeyboardButton("مختبر ميكانيكا الموائع ونقل الحرارة", callback_data=f"{data}_labheat")],
                [InlineKeyboardButton("هيدروليك", callback_data=f"{data}_hyd"), InlineKeyboardButton("إنشاءات", callback_data=f"{data}_const")],
                [InlineKeyboardButton("مواصفات وعقود وحساب كميات", callback_data=f"{data}_spec")],
                [InlineKeyboardButton("الإدارة الهندسية وضبط الجودة", callback_data=f"{data}_mng")],
                [InlineKeyboardButton("تحليل إنشاءات 2", callback_data=f"{data}_struc2"), InlineKeyboardButton("تحليل إنشاءات 1", callback_data=f"{data}_struc1")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="ce"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data.endswith(("ce_do")):
        await query.edit_message_text(
            text="بناء ومدني - اختياري تخصص:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("تصميم رصفات", callback_data=f"{data}_pave")],
                [InlineKeyboardButton("مقدمة في منهجية البحث العلمي", callback_data=f"{data}_resm")],
                [InlineKeyboardButton("منشآت معدنية 2", callback_data=f"{data}_met2")],
                [InlineKeyboardButton("خرسانة 3", callback_data=f"{data}_conc3")],
                [InlineKeyboardButton("تقييم الأثر البيئي", callback_data=f"{data}_envimp")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="ce"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data in SUBJECT_LINKS:
        await query.message.reply_text(
            f"{SUBJECT_LINKS[data]}"
        )

    # ---- Roadmaps ----
    elif data == "cse_roadmaps":
        keyboard = [
            [InlineKeyboardButton("🤖 AI & Machine Learning", url = "https://roadmap.sh/machine-learning")],
            [InlineKeyboardButton("📊 Data Science", url = "https://roadmap.sh/data-engineer"), InlineKeyboardButton("🤖 Robotics", url = "https://qr1.me-qr.com/mobile/pdf/d1770eda-eaec-47c7-aefe-d6b04597d1d9")],
            [InlineKeyboardButton("🔐 Cybersecurity", url = "https://roadmap.sh/cyber-security"), InlineKeyboardButton("🌐 Full Stack Developer", url = "https://roadmap.sh/full-stack")],
            [InlineKeyboardButton("🎨 Frontend", url = "https://roadmap.sh/frontend"), InlineKeyboardButton("🧠 Backend", url = "https://roadmap.sh/backend")],
            [InlineKeyboardButton("📱 iOS Dev", url = "https://roadmap.sh/ios"), InlineKeyboardButton("🧪 QA", url = "https://roadmap.sh/qa"), InlineKeyboardButton("🖌 UX", url = "https://roadmap.sh/ux-design")],
            [InlineKeyboardButton("📱 Android Dev", url = "https://roadmap.sh/android"), InlineKeyboardButton("🎮 Game Developer", url = "https://roadmap.sh/game-developer")],
            [InlineKeyboardButton("⚙ Low Level Programming", url = "https://qr1.me-qr.com/mobile/pdf/42137ab5-0755-4824-9f23-707f8f2e3df0")],
            [InlineKeyboardButton("⚡more tracks roadmaps⚡", url = "https://roadmap.sh")],
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

        # await query.message.reply_text(
        #     "🗺 Roadmaps – هندسة الحاسوب",
        #     reply_markup=InlineKeyboardMarkup([
        #         [InlineKeyboardButton("🔙 رجوع", callback_data="cse_roadmaps"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
        #     ])
        # )

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
            text=  "👋 أهلاً بك في بوت الهندسة الجامعية\n\n"
        "📌 **طريقة استخدام البوت:**\n"
        "• البوت يعمل بالكامل عبر الأزرار.\n"
        "• اختر تخصصك من القائمة الرئيسية.\n"
        "• ادخل إلى قسم المواد ثم اختر نوع المادة.\n"
        "• داخل كل مادة ستجد التلاخيص، الشروحات، الكتب، الامتحانات وغيرها.\n"
        "• يمكنك دائمًا الرجوع باستخدام زر (رجوع).\n\n"
        "تعليمات الاستخدام:\n"
        "/inst\n\n"
        "💡 لأي ملاحظات أو اقتراحات استخدم الأمر:\n"
        "/note\n\n"
        "عن الجمعية، وروابط خارجية:\n"
        "/about\n\n"
        "👇 اختر من القائمة:",
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
    # app.add_handler(CommandHandler("bots", bots))
    app.add_handler(CommandHandler("note", note_command))
    app.add_handler(CommandHandler("about", about))

    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note_text))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
