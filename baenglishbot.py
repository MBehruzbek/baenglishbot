# main.py


import os
import time
import json
import random
import tempfile
import re
from pathlib import Path


try:
    import telebot
    from telebot import types
except Exception as e:
    raise RuntimeError("pyTelegramBotAPI o'rnatilmagan. Terminalda: pip install pyTelegramBotAPI")

try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None  


try:
    from gtts import gTTS
except Exception:
    gTTS = None


try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    REPORTLAB = True
except Exception:
    REPORTLAB = False


TOKEN = "8454028246:AAHQSiqJbDHVF9HuwoPHidUibslzDHGT_nA"
ADMIN_USERNAME = "sultanov190"
DATA_FILE = "data.json"

bot = telebot.TeleBot(TOKEN)


DEFAULT_DATA = {
    "users": {},
    "topics_links": {},
    "pending_setlink": {},
    "created_at": time.time()
}

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=2)
        return DEFAULT_DATA.copy()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA.copy()

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()


def ensure_user(chat_id, username=None):
    key = str(chat_id)
    if key not in data["users"]:
        data["users"][key] = {
            "username": username or "",
            "level": "beginner",
            "points": 0,
            "quizzes": [],
            "topic_idx": 0
        }
        save_data()
    else:
        if username and data["users"][key].get("username") != username:
            data["users"][key]["username"] = username
            save_data()
    return data["users"][key]

def is_admin(user):
    return getattr(user, "username", "") == ADMIN_USERNAME

def detect_language(text: str) -> str:
    
    if re.search(r"[а-яА-ЯёЁғқўҳҒҚЎҲ]", text):
        return "uz"
    
    latin_chars = sum(1 for ch in text if ch.isalpha() and ch.isascii())
    if latin_chars >= max(1, len(text) / 2):
        return "en"
    return "en"

def auto_translate(text: str):
    if GoogleTranslator is None:
        return None
    try:
        lang = detect_language(text)
        if lang == "uz":
            return GoogleTranslator(source='uz', target='en').translate(text)
        else:
            return GoogleTranslator(source='en', target='uz').translate(text)
    except Exception:
        return None

def tts_send(chat_id, text, lang='en'):
    if gTTS is None:
        bot.send_message(chat_id, "gTTS o'rnatilmagan. Terminalda: pip install gtts")
        return
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.close()
        gTTS(text=text, lang=lang).save(tmp.name)
        with open(tmp.name, "rb") as audio:
            bot.send_audio(chat_id, audio)
        os.unlink(tmp.name)
    except Exception as e:
        bot.send_message(chat_id, f"TTS xatosi: {e}")

def generate_vocab_file(level: str, vocab_list):
    fname = f"{level}_vocab"
    if REPORTLAB:
        pdf_name = fname + ".pdf"
        try:
            pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
            font_name = "DejaVuSans"
        except Exception:
            font_name = "Helvetica"
        c = canvas.Canvas(pdf_name, pagesize=A4)
        width, height = A4
        c.setFont(font_name, 12)
        y = height - 40
        c.drawString(40, y, f"{level.capitalize()} Vocabulary ({len(vocab_list)} items)")
        y -= 30
        for i, (eng, uz) in enumerate(vocab_list, 1):
            line = f"{i}. {eng} — {uz}"
            if y < 60:
                c.showPage()
                c.setFont(font_name, 12)
                y = height - 40
            c.drawString(40, y, line)
            y -= 14
        c.save()
        return pdf_name
    else:
        txt_name = fname + ".txt"
        with open(txt_name, "w", encoding="utf-8") as f:
            f.write(f"{level.capitalize()} Vocabulary ({len(vocab_list)} items)\n\n")
            for i, (eng, uz) in enumerate(vocab_list, 1):
                f.write(f"{i}. {eng} — {uz}\n")
        return txt_name


BEGINNER_TOPICS = [
    ("1. To be (am/is/are)", "Be fe'li: hozirgi holatni bildiradi.", ["I am a student.", "She is happy."]),
    ("2. Present Simple", "Odatiy, takroriy harakatlar uchun.", ["I go to school every day.", "He works at a bank."]),
    ("3. Present Continuous", "Hozir bo'layotgan harakatlar (am/is/are + V-ing).", ["I am studying now.", "They are playing."]),
    ("4. Past Simple", "O'tgan zamon (V2 yoki -ed).", ["I visited yesterday.", "She watched TV."]),
    ("5. Future (will / going to)", "Kelajakni ifodalash.", ["I will call you.", "I am going to travel."]),
    ("6. Articles (a/an/the)", "A/An (noaniq), The (ma'lum).", ["A cat, an apple, the sun."]),
    ("7. Plural nouns", "Ko'plik hosil qilish: -s/-es/-ies.", ["One book, two books."]),
    ("8. Wh- questions", "What/Where/When/Who/Why/How.", ["What is your name?", "Where do you live?"]),
    ("9. Prepositions of place", "in/on/at/under/next to.", ["The book is on the table."]),
    ("10. Common adjectives", "Sifatlar: big, small, happy, sad.", ["She is beautiful.", "It is big."])
]

INTERMEDIATE_TOPICS = [
    ("1. Present Perfect", "Have/has + V3: o'tmishdan hozirga ta'siri.", ["I have seen that movie."]),
    ("2. Modal verbs (should/must/might)", "Maslahat, majburiyat, ehtimollik.", ["You should study.", "He must come."]),
    ("3. Passive voice (intro)", "be + V3: qilinayotgan harakatga e'tibor.", ["The letter was sent."]),
    ("4. Conditionals (Type 1 & 2 intro)", "Agar ... bo'lsa ...", ["If it rains, I will stay home."]),
    ("5. Phrasal verbs (common)", "Look after, give up, take off.", ["She gave up smoking."])
]

ADVANCED_TOPICS = [
    ("1. Mixed conditionals", "Murakkab conditional turlari va ularning tahlili.", ["If I had studied, I would be successful now."]),
    ("2. Causatives (have/get sth done)", "Boshqadan ish bajarilishini ifodalash.", ["I had my car repaired."]),
    ("3. Inversion & emphasis", "Emphasis uchun strukturani o'zgartirish.", ["Never have I seen such beauty."]),
    ("4. Advanced phrasal verbs & idioms", "Murakkab idiomatik ifodalar.", ["Break the ice, come up with."]),
    ("5. Academic linking words", "Therefore, however, moreover for coherence.", ["Furthermore, the results show..."])
]

BASE_BEGINNER_VOCAB = [("apple","olma"),("book","kitob"),("pen","qalam"),("chair","stul"),("table","stol"),
                       ("school","maktab"),("teacher","o'qituvchi"),("student","talaba"),("water","suv"),("food","ovqat"),
                       ("dog","it"),("cat","mushuk"),("house","uy"),("car","mashina"),("road","yo'l")]

BASE_INTERMEDIATE_VOCAB = [("opportunity","imkoniyat"),("experience","tajriba"),("responsibility","mas'uliyat"),
                           ("develop","rivojlantirmoq"),("challenge","qiyinchilik")]

BASE_ADVANCED_VOCAB = [("comprehensive","to'liq qamrovli"),("nuance","noziklik"),("meticulous","sinchkov")]

def expand_vocab(base_pairs, target_count):
    vocab = []
    i = 0
    while len(vocab) < target_count:
        eng, uz = base_pairs[i % len(base_pairs)]
        occ = sum(1 for e,_ in vocab if e == eng)
        if occ == 0:
            vocab.append((eng, uz))
        else:
            vocab.append((f"{eng}{occ+1}", uz))
        i += 1
    return vocab

BEGINNER_VOCAB = expand_vocab(BASE_BEGINNER_VOCAB, 300)
INTERMEDIATE_VOCAB = expand_vocab(BASE_INTERMEDIATE_VOCAB, 200)
ADVANCED_VOCAB = expand_vocab(BASE_ADVANCED_VOCAB, 100)


def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🌐 Tarjima", "🔊 Talaffuz")
    kb.add("📘 Grammatika", "📚 Lug‘atlar")
    kb.add("🧠 Quiz", "🎧 Listening")
    kb.add("📅 Daily word", "📊 Profile")
    return kb

def grammar_level_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🟢 Beginner", "🟡 Intermediate", "🔴 Advanced")
    kb.add("🔙 Orqaga")
    return kb

def vocab_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Beginner vocab (PDF/TXT)", "Intermediate vocab (PDF/TXT)")
    kb.add("Advanced vocab (PDF/TXT)", "🔙 Orqaga")
    return kb


@bot.message_handler(commands=['start','help'])
def cmd_start(message):
    ensure_user(message.chat.id, getattr(message.from_user, "username", ""))
    bot.send_message(
        message.chat.id,
        "👋 Assalomu alaykum! Ingliz tili o‘rganish botiga xush kelibsiz.\n"
        "Menyu orqali bo‘limni tanlang yoki bevosita yozing — men avtomatik tarjima qilaman.",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "🌐 Tarjima")
def manual_translate_prompt(message):
    msg = bot.send_message(message.chat.id, "✍️ Tarjima qilinsin deb xohlagan matnni kiriting:")
    bot.register_next_step_handler(msg, manual_translate_step)

def manual_translate_step(message):
    txt = message.text.strip()
    tr = auto_translate(txt)
    if tr:
        bot.send_message(message.chat.id, f"🔁 Tarjima:\n{tr}")
    else:
        bot.send_message(message.chat.id, "Tarjima imkoniyati mavjud emas yoki xatolik yuz berdi.")
    bot.send_message(message.chat.id, "🔙 Asosiy menyu", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "🔊 Talaffuz")
def tts_prompt(message):
    msg = bot.send_message(message.chat.id, "🔈 Talaffuz qilinadigan matnni yuboring:")
    bot.register_next_step_handler(msg, handle_tts)

def handle_tts(message):
    txt = message.text.strip()
    lang = 'en' if detect_language(txt) == 'en' else 'uz'
    tts_send(message.chat.id, txt, lang=lang)
    bot.send_message(message.chat.id, "🔙 Asosiy menyu", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "📘 Grammatika")
def grammar_menu(message):
    bot.send_message(message.chat.id, "Darajani tanlang:", reply_markup=grammar_level_keyboard())

@bot.message_handler(func=lambda m: m.text in ["🟢 Beginner","🟡 Intermediate","🔴 Advanced"])
def grammar_level_selected(message):
    text = message.text
    if text == "🟢 Beginner":
        topics = BEGINNER_TOPICS; level = "beginner"
    elif text == "🟡 Intermediate":
        topics = INTERMEDIATE_TOPICS; level = "intermediate"
    else:
        topics = ADVANCED_TOPICS; level = "advanced"
    kb = types.InlineKeyboardMarkup()
    for idx, (title, _, _) in enumerate(topics):
        short_title = title.split(". ",1)[1] if ". " in title else title
        kb.add(types.InlineKeyboardButton(f"{idx+1}. {short_title}", callback_data=f"topic|{level}|{idx}"))
    kb.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data="grammar_back"))
    bot.send_message(message.chat.id, f"📘 {text} mavzulari:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("topic|"))
def callback_show_topic(call):
    try:
        parts = call.data.split("|")
        _, level, idx_str = parts
        idx = int(idx_str)
        if level == "beginner":
            topics = BEGINNER_TOPICS
        elif level == "intermediate":
            topics = INTERMEDIATE_TOPICS
        else:
            topics = ADVANCED_TOPICS
        title, rule, examples = topics[idx]
        examples_text = "\n".join(f"• {e}" for e in examples)
        kb = types.InlineKeyboardMarkup()
        key = f"{level}_{idx}"
        ylink = data.get("topics_links", {}).get(key)
        if ylink:
            kb.add(types.InlineKeyboardButton("🎬 YouTube darsini ko'rish", url=ylink))
        else:
            kb.add(types.InlineKeyboardButton("🎬 YouTube linki yo'q", callback_data="no_youtube"))
        kb.add(types.InlineKeyboardButton("🔧 (Admin) Link qo'yish", callback_data=f"setlink|{level}|{idx}"))
        kb.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data="grammar_back"))
        bot.send_message(call.message.chat.id, f"📚 *{title}*\n\n📖 *Qoidasi:* {rule}\n\n🧩 *Misollar:*\n{examples_text}", parse_mode="Markdown", reply_markup=kb)
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id, f"Xato: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "no_youtube")
def callback_no_youtube(call):
    bot.answer_callback_query(call.id, "Bu mavzu uchun YouTube linki hali qo‘yilmagan. Agar admin bo‘lsangiz, 'Link qo‘yish' tugmasini bosing.")

@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("setlink|"))
def callback_setlink(call):
    try:
        parts = call.data.split("|")
        _, level, idx_str = parts
        idx = int(idx_str)
        user = call.from_user
        if not is_admin(user):
            bot.answer_callback_query(call.id, "Bu amal faqat admin uchun.")
            return
        data.setdefault("pending_setlink", {})[str(user.id)] = {"level": level, "idx": idx}
        save_data()
        bot.send_message(call.message.chat.id, "🔧 Admin: mavzu uchun YouTube linkini yuboring (http/https bilan).")
        bot.answer_callback_query(call.id, "Link yuborishni kuting.")
    except Exception as e:
        bot.answer_callback_query(call.id, f"Xato: {e}")

@bot.message_handler(func=lambda m: str(m.from_user.id) in data.get("pending_setlink", {}))
def handle_admin_link(message):
    uid = str(message.from_user.id)
    pending = data.get("pending_setlink", {}).get(uid)
    if not pending:
        bot.send_message(message.chat.id, "Kutilayotgan holat topilmadi.")
        return
    if not is_admin(message.from_user):
        bot.send_message(message.chat.id, "Bu amal faqat admin uchun.")
        data["pending_setlink"].pop(uid, None)
        save_data()
        return
    url = message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.send_message(message.chat.id, "Iltimos to'liq URL yuboring (http/https bilan).")
        return
    key = f"{pending['level']}_{pending['idx']}"
    data.setdefault("topics_links", {})[key] = url
    data["pending_setlink"].pop(uid, None)
    save_data()
    bot.send_message(message.chat.id, f"✅ Link saqlandi: {url}")

@bot.callback_query_handler(func=lambda call: call.data == "grammar_back")
def callback_grammar_back(call):
    bot.send_message(call.message.chat.id, "🔙 Darajani tanlang:", reply_markup=grammar_level_keyboard())
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.text == "📚 Lug‘atlar")
def vocab_menu(message):
    bot.send_message(message.chat.id, "Lug'at faylini tanlang:", reply_markup=vocab_keyboard())

@bot.message_handler(func=lambda m: m.text in ["Beginner vocab (PDF/TXT)","Intermediate vocab (PDF/TXT)","Advanced vocab (PDF/TXT)"])
def send_vocab_file(message):
    text = message.text
    if text.startswith("Beginner"):
        level = "beginner"; vocab_list = BEGINNER_VOCAB
    elif text.startswith("Intermediate"):
        level = "intermediate"; vocab_list = INTERMEDIATE_VOCAB
    else:
        level = "advanced"; vocab_list = ADVANCED_VOCAB
    bot.send_message(message.chat.id, f"📥 {level.capitalize()} lug'at fayli yaratilmoqda... Iltimos kuting.")
    fname = generate_vocab_file(level, vocab_list)
    with open(fname, "rb") as f:
        bot.send_document(message.chat.id, f)
    try:
        os.remove(fname)
    except:
        pass
    bot.send_message(message.chat.id, "🔙 Asosiy menyu", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "📅 Daily word")
def daily_word(message):
    eng, uz = random.choice(BEGINNER_VOCAB)
    bot.send_message(message.chat.id, f"📅 Bugungi so'z: *{eng}* — {uz}", parse_mode="Markdown")
    if gTTS:
        try:
            tts_send(message.chat.id, eng, lang='en')
        except:
            pass
    bot.send_message(message.chat.id, "🔙 Asosiy menyu", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "📊 Profile")
def profile(message):
    ensure_user(message.chat.id, getattr(message.from_user, "username", ""))
    u = data["users"].get(str(message.chat.id), {})
    bot.send_message(message.chat.id, f"👤 @{u.get('username','')}\nLevel: {u.get('level','beginner')}\nPoints: {u.get('points',0)}\nQuizlar: {len(u.get('quizzes',[]))}", reply_markup=main_keyboard())


LISTENING_TESTS = {
    "What fruit is red and crunchy?": "apple",
    "Who teaches students?": "teacher",
    "What do you do at night to rest?": "sleep"
}

@bot.message_handler(func=lambda m: m.text == "🎧 Listening")
def listening_start(message):
    q, a = random.choice(list(LISTENING_TESTS.items()))
    msg = bot.send_message(message.chat.id, f"🎧 Savol: {q}\nJavobni yozing:")
    # register next step
    bot.register_next_step_handler(msg, lambda m, correct=a: check_listening(m, correct))

def check_listening(message, correct):
    if message.text.strip().lower() == correct.lower():
        bot.send_message(message.chat.id, "✅ To'g'ri!")
    else:
        bot.send_message(message.chat.id, f"❌ Noto'g'ri. To'g'ri javob: {correct}")
    bot.send_message(message.chat.id, "🔙 Asosiy menyu", reply_markup=main_keyboard())

# Quiz
QUIZ_POOL_BEGINNER = [
    {"q":"What is the English for 'olma'?", "options":["apple","banana","orange"], "a":"apple"},
    {"q":"Choose correct: She ___ a teacher.", "options":["is","are","am"], "a":"is"},
    {"q":"What is the plural of 'book'?", "options":["books","bookes","bok"], "a":"books"}
]
QUIZ_POOL_INTERMEDIATE = [
    {"q":"Complete: I have ___ my homework.", "options":["done","do","did"], "a":"done"}
]
QUIZ_POOL_ADVANCED = [
    {"q":"Which is noun from 'decide'?", "options":["decision","decidable","decisive"], "a":"decision"}
]

@bot.message_handler(func=lambda m: m.text == "🧠 Quiz")
def start_quiz(message):
    ensure_user(message.chat.id, getattr(message.from_user, "username", ""))
    u = data["users"].get(str(message.chat.id), {})
    level = u.get("level", "beginner")
    if level == "beginner":
        pool = QUIZ_POOL_BEGINNER
    elif level == "intermediate":
        pool = QUIZ_POOL_INTERMEDIATE
    else:
        pool = QUIZ_POOL_ADVANCED
    questions = random.sample(pool, min(5, len(pool)))
    uid = str(message.chat.id)
    data["users"][uid]["current_quiz"] = {"questions": questions, "pos": 0, "score": 0}
    save_data()
    send_quiz_question(message.chat.id)

def send_quiz_question(chat_id):
    uid = str(chat_id)
    user = data["users"].get(uid)
    if not user or "current_quiz" not in user:
        bot.send_message(chat_id, "Quiz topilmadi.")
        return
    state = user["current_quiz"]
    pos = state["pos"]
    if pos >= len(state["questions"]):
        score = state["score"]; total = len(state["questions"])
        bot.send_message(chat_id, f"🏁 Quiz tugadi. Natija: {score}/{total}")
        user.setdefault("quizzes", []).append({"score":score,"total":total,"time":time.time()})
        user["points"] = user.get("points",0) + score*10
        user.pop("current_quiz", None)
        save_data()
        bot.send_message(chat_id, "🔙 Asosiy menyu", reply_markup=main_keyboard())
        return
    q = state["questions"][pos]
    kb = types.InlineKeyboardMarkup()
    for i,opt in enumerate(q["options"]):
        kb.add(types.InlineKeyboardButton(opt, callback_data=f"quiz|{uid}|{pos}|{i}"))
    bot.send_message(chat_id, q["q"], reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("quiz|"))
def quiz_answer_callback(call):
    try:
        _, uid, pos_str, idx_str = call.data.split("|")
        pos = int(pos_str); idx = int(idx_str)
        user = data["users"].get(uid)
        if not user or "current_quiz" not in user:
            bot.answer_callback_query(call.id, "Quiz topilmadi.")
            return
        state = user["current_quiz"]
        q = state["questions"][pos]
        chosen = q["options"][idx]
        correct = q["a"]
        if chosen == correct:
            state["score"] += 1
            bot.answer_callback_query(call.id, "✅ To'g'ri!")
            bot.send_message(call.message.chat.id, "✅ To'g'ri!")
        else:
            bot.answer_callback_query(call.id, f"❌ Noto'g'ri. To'g'ri: {correct}")
            bot.send_message(call.message.chat.id, f"❌ Noto'g'ri. To'g'ri: {correct}")
        state["pos"] += 1
        data["users"][uid]["current_quiz"] = state
        save_data()
        send_quiz_question(int(uid))
    except Exception as e:
        bot.answer_callback_query(call.id, f"Xato: {e}")


@bot.message_handler(func=lambda m: True, content_types=['text'])
def fallback_auto_translate(message):
    tr = auto_translate(message.text.strip()) if GoogleTranslator is not None else None
    if tr:
        bot.send_message(message.chat.id, f"🔁 Tarjima:\n{tr}")
        if detect_language(message.text.strip()) == "en":
            try:
                tts_send(message.chat.id, message.text.strip(), lang='en')
            except:
                pass
        return
    bot.send_message(message.chat.id, "Iltimos menyudan bo‘lim tanlang yoki 🌐 Tarjima tugmasini bosing.", reply_markup=main_keyboard())

if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("Bot to‘xtatildi (KeyboardInterrupt).")
    except Exception as e:
        print("Bot xatosi:", e)
