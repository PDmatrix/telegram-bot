from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent, Bot
from threading import Thread
from urllib import parse
import answers, replacements, schedule, hybrid, zvonki
import logging, os, sys, subprocess, psycopg2, requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update, job_queue, chat_data):
    update.message.reply_text(
        'Добро пожаловать!\n'
        'Для получения информации введите /help\n'
        'Для получения комманд введите /command')
    regUser(update.effective_user.id, update.effective_user.username)

def dbQuery(query, *args):
    try:
        parse.uses_netloc.append("postgres")
        dataurl = os.environ.get('DATABASE_URL')
        url = parse.urlparse(dataurl)
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cur = conn.cursor()
        cur.execute(query, args)
        try:
            result = cur.fetchall()
        except:
            result = None
        try:
            conn.commit()
        except:
            pass
    except psycopg2.ProgrammingError as e:
        print('db error')
        print(e)
        result = None
    finally:
        cur.close()
        conn.close()
        return result

def help(bot, update):
    update.message.reply_text(
        'Бот, присылающий ответы по предмету ТБД. Также, он может прислать замены и расписание предметов ЧЭМК.\n'
        'На данный момент доступны замены всех групп, но расписание только группы ПР1-15.\n'
        'Для получения списка и описания комманд введите /command')

def command(bot, update, args):
    update.message.reply_text(
        '/sch [день] - Расписание. По умолчанию возвращает расписание на завтра.\n'
        'Принимает один необязательный аргумент.\n'
        '[день] = \'пн\',\'вт\',\'ср\',\'чт\',\'пт\',\'сб\',\'завтра\',\'сегодня\'\n'
        '\n/rep [день] [группа] - Замены. По умолчанию возвращает замены группы Пр1-15 на завтра.\n'
        'Принимет два необязательных аргумента в любой последовательности.\n'
        '[день] = \'сегодня\', \'завтра\'\n'
        '[группа] = Группы ЧЭМК\n'
        '\n/hyb [день] [группа] - Расписание с заменами. По умолчанию возвращает расписание группы Пр1-15 на завтра\n'
        'Принимает два необязательных аргумента в любой последовательности.\n'
        '[день] = \'сегодня\', \'завтра\'\n'
        '[группа] = Группы ЧЭМК. На данный момент только Пр1-15')

def regUser(userid, username):
    here = dbQuery("SELECT id FROM users")
    newHere = []
    for i in range(0, len(here)):
        newHere.insert(0,here[i][0])
    here = newHere
    try:
        if userid not in here:
            dbQuery("INSERT INTO users (id, name, note) VALUES (%s,%s,0)",userid,username)
    except IndexError:
        dbQuery("INSERT INTO users (id, name, note) VALUES (%s,%s,0)", userid,username)

def sch(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    day = "завтра"
    if len(args) == 1:
        day = args[0].lower()
    update.message.reply_text(schedule.getSchedule(day))
    regUser(update.effective_user.id, update.effective_user.username)
    

def hyb(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    gr = "пр1-15"
    time = "завтра"
    if len(args) == 2:
        if args[0] == "завтра" or args[0] == "сегодня":
            time = args[0]
            gr = args[1]
        else:
            time = args[1]
            gr = args[0]
    elif len(args) == 1:
        if args[0] == "завтра" or args[0] == "сегодня":
            time = args[0]
        else:
            gr = args[0]
    update.message.reply_text(hybrid.getHybrid(gr,time))

    regUser(update.effective_user.id, update.effective_user.username)
    
def rep(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    gr = "пр1-15"
    time = "завтра"
    if len(args) == 2:
        if args[0] == "завтра" or args[0] == "сегодня":
            time = args[0]
            gr = args[1]
        else:
            time = args[1]
            gr = args[0]
    elif len(args) == 1:
        if args[0] == "завтра" or args[0] == "сегодня":
            time = args[0]
        else:
            gr = args[0]
    update.message.reply_text(replacements.findChange(gr,time))

    regUser(update.effective_user.id, update.effective_user.username)
    
def echo(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    ans = answers.getAnswer(update.message.text)
    for i in range(0, len(ans), 2):
        update.message.reply_text(ans[i] + ans[i + 1])
        if i > 10:
            update.message.reply_text("Очень много ответов. Задайте более точный вопрос.")
            break
    if len(ans) == 0:
        update.message.reply_text("Вопрос не найден.")

    regUser(update.effective_user.id, update.effective_user.username)

def note(bot, job):
    global ss
    rp = replacements.findChange("пр1-15","завтра")
    if rp != ss and rp != "Сервер недоступен." and rp != "Нет замен." and rp != "Что-то не так. Проверьте замены вручную." and rp != "Расписание не готово.":
        ids = dbQuery("SELECT id FROM users WHERE note = 1")
        try:
          for i in range(0, len(ids)):
            bot.send_message(ids[i][0], text = rp)
        except Exception as e:
          print(e)
        ss = rp
        
def setNote(bot, update, job_queue, chat_data):  
    chat_id = update.message.chat_id
    global ss
    job = job_queue.run_repeating(note, interval=60, context=chat_id)
    chat_data['job'] = job
    update.message.reply_text('Таймер на уведомление установлен!')
    ss = replacements.findChange("пр1-15","завтра")
    dbQuery("UPDATE users SET note = 1 WHERE id = %s" , (chat_id))

def unsetNote(bot, update, chat_data):
    chat_id = update.message.chat_id
    if 'job' not in chat_data:
        update.message.reply_text('Таймер не установлен')
        return
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    update.message.reply_text('Таймер удалён!')
    dbQuery("UPDATE users SET note = 0 WHERE id = %s" , (chat_id))

def checkNote(bot, update, chat_data):
    if 'job' not in chat_data:
        update.message.reply_text('Таймер не установлен')
        return
    else:
        update.message.reply_text('Таймер установлен')
        return
    
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def onStart(bot, chat_data, job_queue):
    ids = dbQuery("SELECT id FROM users WHERE note = 1")
    try:
        for i in range(0, len(ids)):
            global ss
            ss = replacements.findChange("пр1-15","завтра")
            job = job_queue.run_repeating(note, interval = 60, context = ids[i][0])
            chat_data[ids[i][0] if ids[i][0] not in chat_data else None]['job'] = job
    except Exception as e:
        print(e)

def stop_and_restart():
        updater.stop()
        subprocess.call(["python", os.path.join(sys.path[0], __file__)] + sys.argv[1:])

def restart(bot, update):
        update.message.reply_text('Бот перезапускается...')
        Thread(target=stop_and_restart).start()

def main():
    TOKEN = os.environ.get('TOKEN')
    updater = Updater(TOKEN)
    bt = Bot(TOKEN)
    dp = updater.dispatcher
    onStart(bt, dp.chat_data, dp.job_queue)
    dp.add_handler(CommandHandler("start", start,pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rep", rep, pass_args=True))
    dp.add_handler(CommandHandler("sch", sch, pass_args=True))
    dp.add_handler(CommandHandler("hyb", hyb, pass_args=True))
    dp.add_handler(CommandHandler("command", command, pass_args=True))
    dp.add_handler(CommandHandler("set", setNote, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unsetNote, pass_chat_data=True))
    dp.add_handler(CommandHandler("check", checkNote, pass_chat_data=True))

    dp.add_handler(CommandHandler('rs', restart, filters=Filters.user(username='@Dmatrix')))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
