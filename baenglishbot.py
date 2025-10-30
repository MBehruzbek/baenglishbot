import telebot
from telebot import types

# Telegram token
TOKEN = "8454028246:AAHQSiqJbDHVF9HuwoPHidUibslzDHGT_nA"
bot = telebot.TeleBot(TOKEN)

# Umumiy YouTube playlist
YOUTUBE_PLAYLIST = "https://www.youtube.com/playlist?list=PLkREkayoYCyI9KGsZ2TfeVccRv9qP0gl"

# Foydalanuvchi ma'lumotlari
user_data = {}

# Beginner grammatika
beginner_grammar = {
    "1. Articles (a, an, the)": {
        "description": "Artikllar narsalarni aniqlash uchun ishlatiladi.",
        "explanation": "‘a’ undosh bilan, ‘an’ unli bilan, ‘the’ aniq narsalar uchun.",
        "examples": [
            ["A dog is cute.", "Bir it yoqimli."],
            ["An apple is red.", "Bir olma qizil."],
            ["The sun is bright.", "Quyosh yorqin."]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "2. Plural Forms": {
        "description": "Otlarni ko‘p holatda ifodalash.",
        "explanation": "Ko‘p otlar ‘-s’ yoki ‘-es’ bilan yasaladi.",
        "examples": [
            ["One book, two books.", "Bir kitob, ikki kitob."],
            ["One child, two children.", "Bir bola, ikki bola."],
            ["One box, two boxes.", "Bir quti, ikki quti."]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "3. Adjectives": {
        "description": "Sifatlar narsalarni tasvirlaydi.",
        "explanation": "Sifatlar otlardan oldin keladi.",
        "examples": [
            ["A big house.", "Katta uy."],
            ["She is happy.", "U xursand."],
            ["This is a beautiful flower.", "Bu chiroyli gul."]
        ],
        "video": YOUTUBE_PLAYLIST
    }
}

# Intermediate grammatika
intermediate_grammar = {
    "1. Conditional Sentences": {
        "description": "Shart gaplar.",
        "explanation": "Zero: haqiqatlar (If + Present, Present). First: kelajak (If + Present, will + V1).",
        "examples": [
            ["If you heat water, it boils.", "Suvni isitsangiz, qaynaydi."],
            ["If it rains, I will stay home.", "Yomg‘ir yog‘sa, uyda qolaman."],
            ["If I study, I pass.", "O‘qisam, o‘taman."]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "2. Passive Voice": {
        "description": "Passiv holat.",
        "explanation": "Subject + to be + V3.",
        "examples": [
            ["The book is read by me.", "Kitob men tomonimdan o‘qiladi."],
            ["The house was built.", "Uy qurildi."],
            ["The cake will be eaten.", "Tort yeyiladi."]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "3. Reported Speech": {
        "description": "Bilvosita gap.",
        "explanation": "Fe’l zamonlari o‘zgaradi (Present → Past).",
        "examples": [
            ["She said, ‘I am tired.’", "U aytdi: ‘Men charchadim.’"],
            ["He said he was tired.", "U charchaganini aytdi."],
            ["They asked, ‘Are you coming?’", "Ular so‘radilar: ‘Kelyapsizmi?’"]
        ],
        "video": YOUTUBE_PLAYLIST
    }
}

# Advanced grammatika
advanced_grammar = {
    "1. Modal Verbs": {
        "description": "Modal fe’llar: ehtimollik, maslahat.",
        "explanation": "‘might’ ehtimollik, ‘should’ maslahat uchun.",
        "examples": [
            ["She might come tomorrow.", "U ertaga kelishi mumkin."],
            ["You should study harder.", "Qattiqroq o‘qishingiz kerak."],
            ["He could have won.", "U yutishi mumkin edi."]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "2. Inversion": {
        "description": "So‘z tartibini ta’kidlash uchun o‘zgartirish.",
        "explanation": "Ega va fe’l o‘rni almashadi.",
        "examples": [
            ["Never have I seen such beauty.", "Bunday go‘zallikni ko‘rmaganman."],
            ["Only then did he understand.", "Faqat o‘shanda tushundi."],
            ["Had I known, I would have helped.", "Bilsam, yordam bergan bo‘lardim."]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "3. Subjunctive Mood": {
        "description": "Faraziy holatlar uchun.",
        "explanation": "Orzu, faraz yoki talab uchun ishlatiladi.",
        "examples": [
            ["I wish I were taller.", "Balandroq bo‘lsam edi."],
            ["It’s vital that she be here.", "Uning bu yerda bo‘lishi muhim."],
            ["If he were here, we’d talk.", "U bu yerda bo‘lsa, gaplashardik."]
        ],
        "video": YOUTUBE_PLAYLIST
    }
}

# Beginner mavzular (1–10)
beginner_topics = {
    "1. Greetings and Introductions": {
        "description": "Salomlashish va tanishish so‘zlari.",
        "words": [
            ["hello", "salom"], ["hi", "salom"], ["good morning", "xayrli tong"], ["good afternoon", "xayrli kun"], ["good evening", "xayrli kech"],
            ["goodbye", "xayr"], ["please", "iltimos"], ["thank you", "rahmat"], ["sorry", "kechirasiz"], ["excuse me", "uzr"],
            ["my name is", "mening ismim"], ["nice to meet you", "tanishganimdan xursandman"], ["how are you", "yaxshimisiz"], ["I'm fine", "men yaxshiman"], ["friend", "do‘st"]
        ],
        "video": "https://www.youtube.com/watch?v=7v2G99ZptmU"
    },
    "2. Numbers": {
        "description": "Raqamlar va ularga bog‘liq so‘zlar.",
        "words": [
            ["one", "bir"], ["two", "ikki"], ["three", "uch"], ["four", "to‘rt"], ["five", "besh"],
            ["six", "olti"], ["seven", "yetti"], ["eight", "sakkiz"], ["nine", "to‘qqiz"], ["ten", "o‘n"],
            ["hundred", "yuz"], ["thousand", "ming"], ["million", "million"], ["count", "hisoblamoq"], ["number", "raqam"]
        ],
        "video": "https://www.youtube.com/watch?v=5r5z4vM3p8Y"
    },
    "3. Colors": {
        "description": "Ranglar va tasvirlash so‘zlari.",
        "words": [
            ["red", "qizil"], ["blue", "ko‘k"], ["green", "yashil"], ["yellow", "sariq"], ["black", "qora"],
            ["white", "oq"], ["pink", "pushti"], ["purple", "binafsha"], ["orange", "apelsin rangi"], ["brown", "jigarrang"],
            ["gray", "kulrang"], ["dark", "qoramtir"], ["light", "och"], ["bright", "yorqin"], ["color", "rang"]
        ],
        "video": "https://www.youtube.com/watch?v=9v2G99ZptmU"
    },
    "4. Family": {
        "description": "Oila a’zolari.",
        "words": [
            ["family", "oila"], ["mother", "ona"], ["father", "ota"], ["brother", "aka"], ["sister", "opa"],
            ["grandmother", "buvim"], ["grandfather", "bobom"], ["aunt", "xola"], ["uncle", "amaki"], ["cousin", "amaki/bola"],
            ["son", "o‘g‘il"], ["daughter", "qiz"], ["husband", "er"], ["wife", "xotin"], ["parent", "ota-ona"]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "5. Food and Drinks": {
        "description": "Ovqatlar va ichimliklar.",
        "words": [
            ["food", "ovqat"], ["drink", "ichimlik"], ["breakfast", "nonushta"], ["lunch", "tushlik"], ["dinner", "kechki ovqat"],
            ["bread", "non"], ["rice", "guruch"], ["meat", "go‘sht"], ["fish", "baliq"], ["chicken", "tovuq"],
            ["water", "suv"], ["milk", "sut"], ["tea", "choy"], ["coffee", "kofe"], ["juice", "sharbat"]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "6. Clothes": {
        "description": "Kiyimlar va moda.",
        "words": [
            ["clothes", "kiyim"], ["shirt", "ko‘ylak"], ["pants", "shim"], ["dress", "ko‘ylak (ayollar)"], ["jacket", "kurtka"],
            ["shoes", "poyabzal"], ["hat", "shlyapa"], ["scarf", "sharfa"], ["gloves", "qo‘lqop"], ["socks", "paypoq"],
            ["belt", "kamar"], ["jeans", "jins"], ["t-shirt", "futbolka"], ["wear", "kiymoq"], ["fashion", "moda"]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "7. House and Furniture": {
        "description": "Uy va mebellar.",
        "words": [
            ["house", "uy"], ["room", "xona"], ["kitchen", "oshxona"], ["bedroom", "yotoqxona"], ["bathroom", "vanna xonasi"],
            ["table", "stol"], ["chair", "stul"], ["bed", "karavot"], ["sofa", "divan"], ["wardrobe", "shkaf"],
            ["window", "deraza"], ["door", "eshik"], ["carpet", "gilam"], ["lamp", "chiroq"], ["mirror", "oyna"]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "8. Daily Activities": {
        "description": "Kundalik faoliyatlar.",
        "words": [
            ["wake up", "uyg‘onmoq"], ["get up", "turmoq"], ["brush teeth", "tish yuvmoq"], ["take a shower", "dush qilmoq"], ["get dressed", "kiyinish"],
            ["eat breakfast", "nonushta qilmoq"], ["study", "o‘qimoq"], ["work", "ishlamoq"], ["relax", "dam olmoq"], ["watch TV", "televizor ko‘rmoq"],
            ["read", "o‘qimoq"], ["write", "yozmoq"], ["sleep", "uxlamoq"], ["eat", "yemoq"], ["walk", "yurmoq"]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "9. Weather": {
        "description": "Ob-havo so‘zlari.",
        "words": [
            ["weather", "ob-havo"], ["sunny", "quyoshli"], ["cloudy", "bulutli"], ["rainy", "yomg‘irli"], ["windy", "shamolli"],
            ["hot", "issiq"], ["cold", "sovuq"], ["warm", "iliq"], ["rain", "yomg‘ir"], ["snow", "qor"],
            ["wind", "shamol"], ["cloud", "bulut"], ["sun", "quyosh"], ["storm", "bo‘ron"], ["temperature", "harorat"]
        ],
        "video": YOUTUBE_PLAYLIST
    },
    "10. Animals": {
        "description": "Hayvonlar so‘zlari.",
        "words": [
            ["animal", "hayvon"], ["dog", "it"], ["cat", "mushuk"], ["bird", "qush"], ["fish", "baliq"],
            ["horse", "ot"], ["cow", "sigir"], ["sheep", "qo‘y"], ["lion", "sher"], ["tiger", "yo‘lbars"],
            ["elephant", "fil"], ["monkey", "maymun"], ["bear", "ayiq"], ["pet", "uy hayvoni"], ["zoo", "hayvonot bog‘i"]
        ],
        "video": YOUTUBE_PLAYLIST
    }
}

# Intermediate mavzular
intermediate_topics = {
    "1. Daily Routines": {
        "description": "Kundalik ishlarni tasvirlash.",
        "words": [
            ["wake up", "uyg‘onmoq"], ["get up", "turmoq"], ["brush teeth", "tish yuvmoq"], ["take a shower", "dush qilmoq"], ["get dressed", "kiyinish"],
            ["eat breakfast", "nonushta qilmoq"], ["go to work", "ishga ketmoq"], ["study", "o‘qimoq"], ["exercise", "mashq qilmoq"], ["relax", "dam olmoq"],
            ["watch TV", "televizor ko‘rmoq"], ["read a book", "kitob o‘qimoq"], ["go to bed", "yotmoq"], ["schedule", "jadval"], ["habit", "odat"]
        ],
        "video": YOUTUBE_PLAYLIST
    }
}

# Advanced mavzular
advanced_topics = {
    "1. Business English": {
        "description": "Biznes muhitida so‘zlar.",
        "words": [
            ["business", "biznes"], ["company", "kompaniya"], ["client", "mijoz"], ["contract", "shartnoma"], ["meeting", "uchrashuv"],
            ["presentation", "taqdimot"], ["negotiation", "muzokara"], ["deal", "kelishuv"], ["profit", "foyda"], ["loss", "zarar"],
            ["market", "bozor"], ["strategy", "strategiya"], ["goal", "maqsad"], ["project", "loyiha"], ["deadline", "muddat"]
        ],
        "video": YOUTUBE_PLAYLIST
    }
}

# Inline tugmalar
def create_level_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Beginner", callback_data="level_beginner"))
    markup.add(types.InlineKeyboardButton("Intermediate", callback_data="level_intermediate"))
    markup.add(types.InlineKeyboardButton("Advanced", callback_data="level_advanced"))
    return markup

def create_category_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Grammatika", callback_data="category_grammar"))
    markup.add(types.InlineKeyboardButton("So‘zlar", callback_data="category_words"))
    return markup

def create_topic_buttons(topics):
    markup = types.InlineKeyboardMarkup()
    for topic in topics:
        markup.add(types.InlineKeyboardButton(topic, callback_data=f"topic_{topic}"))
    return markup

def create_grammar_buttons(grammar):
    markup = types.InlineKeyboardMarkup()
    for topic in grammar:
        markup.add(types.InlineKeyboardButton(topic, callback_data=f"grammar_{topic}"))
    return markup

# Start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Ingliz tilini o‘rganish darajasini tanlang:", reply_markup=create_level_buttons())

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id

    if call.data.startswith("level_"):
        level = call.data.split("_")[1]
        user_data[user_id] = {"level": level}
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Nega ingliz tilini o‘rganmoqchisiz? Sababingizni yozing:")
        bot.register_next_step_handler(call.message, save_reason)

    elif call.data.startswith("category_"):
        category = call.data.split("_")[1]
        level = user_data.get(user_id, {}).get("level")
        if not level:
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Iltimos, avval darajani tanlang (/start).")
            return
        bot.answer_callback_query(call.id)
        
        if category == "grammar":
            if level == "beginner":
                bot.send_message(call.message.chat.id, "Beginner grammatika:", reply_markup=create_grammar_buttons(beginner_grammar))
            elif level == "intermediate":
                bot.send_message(call.message.chat.id, "Intermediate grammatika:", reply_markup=create_grammar_buttons(intermediate_grammar))
            elif level == "advanced":
                bot.send_message(call.message.chat.id, "Advanced grammatika:", reply_markup=create_grammar_buttons(advanced_grammar))
            else:
                bot.send_message(call.message.chat.id, "Noto‘g‘ri daraja tanlandi. /start bilan qayta boshlang.")
        
        elif category == "words":
            if level == "beginner":
                bot.send_message(call.message.chat.id, "Beginner mavzulari:", reply_markup=create_topic_buttons(beginner_topics))
            elif level == "intermediate":
                bot.send_message(call.message.chat.id, "Intermediate mavzulari:", reply_markup=create_topic_buttons(intermediate_topics))
            elif level == "advanced":
                bot.send_message(call.message.chat.id, "Advanced mavzulari:", reply_markup=create_topic_buttons(advanced_topics))
            else:
                bot.send_message(call.message.chat.id, "Noto‘g‘ri daraja tanlandi. /start bilan qayta boshlang.")

    elif call.data.startswith("topic_"):
        topic = call.data.replace("topic_", "")
        level = user_data.get(user_id, {}).get("level")
        if not level:
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Iltimos, avval darajani tanlang (/start).")
            return
        bot.answer_callback_query(call.id)
        
        if level == "beginner":
            data = beginner_topics.get(topic)
        elif level == "intermediate":
            data = intermediate_topics.get(topic)
        elif level == "advanced":
            data = advanced_topics.get(topic)
        else:
            bot.send_message(call.message.chat.id, "Noto‘g‘ri daraja tanlandi. /start bilan qayta boshlang.")
            return
        
        if data:
            response = f"**Mavzu: {topic}**\n\n**Tavsif**: {data['description']}\n\n**So‘zlar**:\n"
            for word, translation in data['words']:
                response += f"- {word} — {translation}\n"
            response += f"\n**Video**: {data['video']}"
            bot.send_message(call.message.chat.id, response)
        else:
            bot.send_message(call.message.chat.id, f"Mavzu '{topic}' topilmadi. Boshqa mavzuni tanlang.")

    elif call.data.startswith("grammar_"):
        topic = call.data.replace("grammar_", "")
        level = user_data.get(user_id, {}).get("level")
        if not level:
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Iltimos, avval darajani tanlang (/start).")
            return
        bot.answer_callback_query(call.id)
        
        if level == "beginner":
            data = beginner_grammar.get(topic)
        elif level == "intermediate":
            data = intermediate_grammar.get(topic)
        elif level == "advanced":
            data = advanced_grammar.get(topic)
        else:
            bot.send_message(call.message.chat.id, "Noto‘g‘ri daraja tanlandi. /start bilan qayta boshlang.")
            return
        
        if data:
            response = f"**Grammatika: {topic}**\n\n**Tavsif**: {data['description']}\n\n**Tushuntirish**: {data['explanation']}\n\n**Misollar**:\n"
            for eng, uzb in data['examples']:
                response += f"- {eng} — {uzb}\n"
            response += f"\n**Video**: {data['video']}"
            bot.send_message(call.message.chat.id, response)
        else:
            bot.send_message(call.message.chat.id, f"Grammatika mavzusi '{topic}' topilmadi. Boshqa mavzuni tanlang.")

# Sababni saqlash
def save_reason(message):
    user_id = message.from_user.id
    user_data[user_id]["reason"] = message.text
    bot.send_message(message.chat.id, f"Rahmat! Sababingiz: {message.text}\nO‘rganish turini tanlang:", reply_markup=create_category_buttons())

# Botni ishga tushirish
print("Bot ishga tushdi")
bot.polling()
