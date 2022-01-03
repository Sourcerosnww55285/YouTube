import telebot
from telebot import types
import os
from time import sleep
import pytube
from pytube.helpers import safe_filename
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

token = '5020604343:AAF3Gu7nPagZ19ATiDimEyxYbKODqUIJItA'
bot = telebot.TeleBot(token)
import pytz
from datetime import datetime
import requests
dt_format = '%Y-%m-%d --- %H:%M:%S'
tz = pytz.timezone('Asia/Riyadh')
jt = datetime.now(tz)
time_now = (jt.strftime(dt_format))
print(time_now)
#140 mp4 audio
#18 360p
#22 720p

@bot.message_handler(content_types=["text"], func=lambda message: message.text == "🌐 تحميل مرة اخرى 🌐")
@bot.message_handler(commands=['start'])
def start (message):
    if message.chat.type == 'private':
        ch = "aoo1_1" 
        idu = message.chat.id
        join = requests.get(f"https://api.telegram.org/bot{token}/getChatMember?chat_id=@{ch}&user_id={idu}").text
        if '"language_code":"ar"' in join:
            if '"status":"left"' in join:
                bot.send_message((message.chat.id),'''🚧┇عذراً، عليک الاشتراك في قناة البوت أولاً،
        🚧┇معرف القناة ~⪼ ❨@'''+ch+'''❩
        🔑┇بعد الاشتراک اضغط ❪ /start ❫''')
            else:
                name = (message.chat.first_name)
                markup = types.ForceReply(selective=False)
                link_bot = bot.send_message(message.chat.id,f'<strong>اهلين {name}! من فضلك أرسل لي رابط لتحميله 🪄 </strong>\n \n Me - @rwwwr / My Channel  - @@aoo1_1 🔮💜',parse_mode='HTML')
                with open ('id.txt' , 'r+') as data:
                    file = data.read()
                    search = (str(message.chat.id))
                    if (str(search)) in file:
                        print ('data exits!')
                    else:
                        data.write(str(message.chat.id))
                        data.write(str('\n'))
                        data.close
                        print('i got a new data!')
                bot.register_next_step_handler(link_bot,Defind)
        else:
            if '"status":"left"' in join:
                bot.send_message((message.chat.id),'''🚧┇Sorry, You Have To Subscribe To The Bot Channel First.
                    🚧┇Channel User~⪼ ❨@@aoo1_1❩
                    🔑┇ After Subscribing, Press ❪ /start ❫''')
            else:
                name = (message.chat.first_name)
                markup = types.ForceReply(selective=False)
                link_bot = bot.send_message(message.chat.id,f'<strong>Hey {name}! Please Send Me Link To Download It 🪄 </strong>\n \n Me - @rwwwr / My Channel  - @@aoo1_1 🔮💜',parse_mode='HTML')
                with open ('id.txt' , 'r+') as data:
                    file = data.read()
                    search = (str(message.chat.id))
                    if (str(search)) in file:
                        print ('data exits!')
                    else:
                        data.write(str(message.chat.id))
                        data.write(str('\n'))
                        data.close
                        print('i got a new data!')
                
                bot.register_next_step_handler(link_bot,tybey)

def tybey (message):
    global link_bot
    link_bot = message.text
    print(link_bot)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text="🔊 صوت 🔊")
    button2 = types.KeyboardButton(text="🎞 فيديو 🎞")
    keyboard.add(button1, button2) 
    tybe = bot.send_message(message.chat.id,'<strong>رجاءا اختر واحد من الخيارات بالأسفل 🌐</strong> \n',parse_mode='HTML',reply_markup=keyboard)


@bot.message_handler(content_types=["text"], func=lambda message: message.text == "🔊 صوت 🔊")
def download(message):
    bot.send_message(message.chat.id,'رجاء انتظر ')
    tz = pytz.timezone('Asia/Riyadh')
    jt = datetime.now(tz)
    time_now = (jt.strftime(dt_format))
    print(link_bot)    
    yt = pytube.YouTube(link_bot)
    time = (yt.length / 60)
    

    try:
        bot.send_message(message.chat.id,f"*🌐 العنوان : {yt.title} \n 📺 المشاهدات : {yt.views} \n ⏳ الطول : {time}~  دقيقة ",parse_mode='markdown')
    except:
        pass
    try:
        stream = yt.streams.get_by_itag(140)
    except:
        bot.send_message(message.chat.id,"لم اجده")
    try:
        print('under download')
        key = (f'{yt.views}.mp4')
        print(key)
        stream.download(filename=key)
        sleep(5)
        print('download done')
        
    except:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id,'لقد دخلت في مشكلة) ؛ [مشكلة في التنزيل] ، * حاول مرة أخرى بعد 3-5 دقائق باستخدام /start والتحقق /help للحصول على مزيد من المعلومات! \ n ألا تزال لا تعمل؟ قل لي @rwwwr *',parse_mode='markdown')
        return start
    try:
        with open(key, 'rb') as video:
            bot.send_audio(message.chat.id, video, title=(yt.title),performer='@YRRY2BOT')
            keyboard = types.ReplyKeyboardMarkup()
            button1 = types.KeyboardButton(text="🌐 تحميل مرة اخرى 🌐")
            keyboard.add(button1) 
            bot.send_message(message.chat.id,'*تم تحميله بواسطة @YRRY2BOT ✅!*',parse_mode='markdown',reply_markup=keyboard)
            video.close
            os.remove(key)
        save = open ('downloaded.txt','a+')
        save.write(str(f'[{link_bot}] --- [{yt.title}] -------------- تم تحميله بواسطة [@{message.chat.username}] في [{time_now}] (صوت 🔊)\n'))
        save.close
    except:
        bot.send_message(message.chat.id,'*لا يمكن تحميل الفيديو لان حجمه 50MB+ ⚒*',parse_mode='markdown')
        os.remove(key)


@bot.message_handler(content_types=["text"], func=lambda message: message.text == "🎞 فيديو 🎞")
def downloadV(message):
    bot.send_message(message.chat.id,'رجاء انتظر ')
    tz = pytz.timezone('Asia/Riyadh')
    jt = datetime.now(tz)
    time_now = (jt.strftime(dt_format))
    print(link_bot)    
    yt = pytube.YouTube(link_bot)
    time = (yt.length / 60)
    

    try:
        bot.send_message(message.chat.id,f"*🌐 العنوان : {yt.title} \n 📺 المشاهدات : {yt.views} \n ⏳ الطول : {time}~  دقيقة \n 🌟 التقييم : {yt.rating}",parse_mode='markdown')
    except:
        pass
    
    try:
        stream = yt.streams.get_by_itag(18)
    except:
        bot.send_message(message.chat.id,"لم اجده")

    try:
        print('under download')
        key = (f'{yt.views}.mp4')
        print(key)
        stream.download(filename=key)
        sleep(5)
        print('download done')
        
    except:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id,'لقد دخلت في مشكلة) ؛ [مشكلة في التنزيل] ، * حاول مرة أخرى بعد 3-5 دقائق باستخدام /start والتحقق /help للحصول على مزيد من المعلومات! \n ألا تزال لا تعمل؟ قل لي @rwwwr *',parse_mode='markdown')
        return start
    try:
        with open(key, 'rb') as video:
            print("i'am in key")
            bot.send_video(message.chat.id, video)
            startc = types.ReplyKeyboardMarkup()
            startc1 = types.KeyboardButton(text="🌐 تحميل مرة اخرى 🌐")
            startc.add(startc1)
            bot.send_message(message.chat.id,'*تم تحميله بواسطة @YRRY2BOT ✅!*',parse_mode='markdown',reply_markup=startc)
            video.close
            os.remove(key)
        save = open ('downloaded.txt','a+')
        save.write(str(f'[{link_bot}] --- [{yt.title}] -------------- تم تحميله بواسطة [@{message.chat.username}] في [{time_now}] (فيديو 🔊)\n'))
        save.close
    except:
        bot.send_message(message.chat.id,'*لا يمكن تحميل الفيديو لان حجمه 50MB+ ⚒*',parse_mode='markdown')
        os.remove(key)

def gen_markup():
    with open('id.txt','r') as u:
        lineIDs = 0
        for line in u:
            lineIDs += 1
            lineID = (str(lineIDs))
            u.close
    with open('downloaded.txt','r') as dv:
        line_land = 0
        for line in dv:
            line_land +=1
            lineDv = (int(line_land))
            dv.close
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(f'لدينا الان {lineID} مستخدم 🧝', callback_data="id"),
                               InlineKeyboardButton(f'لدينا الان {lineDv} فيديو تحمل 🃏', callback_data="dv"))
    return markup


@bot.message_handler(commands=['admin'])
def admin (message):
    if message.chat.id == 1197106808 or 723051294:
        bot.reply_to(message,f'<strong>Hi Dad 🧛🏻!</strong> \n\n<ins>لاوامر الادمن الاخرى شيك 💈:</ins> \n/send - اذاعة 📻 \n/file - ملفات البوت 🗂 \n/delete - لمسح ملف الفيديوهات المحملة ⚠️',parse_mode='html',reply_markup=gen_markup())

    else:
        bot.send_message(message.chat.id,'*امر ادمن!*',parse_mode='markdown')

@bot.message_handler(commands=['file'])
def file(message):
    if message.chat.id == 1197106808 or 723051294:
        py = open ('yt download.py','rb')
        bot.send_document(message.chat.id,py,caption='*ملف البوت 🛠!*',parse_mode='markdown')
        iddoc = open('id.txt', 'rb')
        bot.send_document(message.chat.id, iddoc,caption='*الايديات 🌀!*',parse_mode='markdown')
        dvdoc = open('downloaded.txt', 'rb')
        bot.send_document(message.chat.id, dvdoc,caption='*الفيديوهات ♻️!*',parse_mode='markdown')
    else:
        bot.send_message(message.chat.id,'*امر ادمن!*',parse_mode='markdown')
@bot.message_handler(commands=['delete'])
def delete (message):
    bot.send_message(message.chat.id,'متاكد تبغا تمسحه؟ ارسل /sure ☢️')
@bot.message_handler(commands=['sure'])
def sure (message):
    if message.chat.id == 1197106808:
        tz = pytz.timezone('Asia/Riyadh')
        jt = datetime.now(tz)
        time_now = (jt.strftime(dt_format))
        bot.send_message(message.chat.id,'تم مسح الملف 📛')
        os.remove('downloaded.txt')
        idk = open ('downloaded.txt','w')
        idk.write(f'#####$#####This Is [downloaded.txt] File ,it made at {time_now} --- The Old File Has Been Deleted!#####$##### \n')
        idk.close
    else:
        bot.send_message(message.chat.id,'*امر ادمن!*',parse_mode='markdown')


@bot.message_handler(commands=['send'])
def send (message):
    if message.chat.id == 1197106808: 
        text = bot.send_message(message.chat.id,'*ارسل نص الاذاعة ⚜️!*',parse_mode='markdown')
        bot.register_next_step_handler(text,texts)
    else:
        bot.send_message(message.chat.id,'*امر ادمن!*',parse_mode='markdown')
def texts (message):
    done = 0
    passed = 0
    text = message.text
    print(text)
    file = open('id.txt','r')
    for line in file:
        try:
            idn = line
            bot.send_message((idn),(text))
            print('Done For',idn)
            done += 1 
        except:
            pass
            print('passed',idn)
            passed += 1
    file.close
    print('done')
    bot.send_message(message.chat.id,f"<strong>تم الارسال ⚠️ </strong> التفاصيل 📊: \n انرسلت الى <pre>[{done}]</pre> ✅ \n ما اترسلت الى<pre>[{passed}]</pre> ❌\n \n <strong>لارسال رسالة اخرى ارسل /send ⚜️</strong>",parse_mode='html')
             
print('Started!')
bot.infinity_polling()
