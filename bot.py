from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, Bot
from threading import Thread
from urllib import parse
import answers
import replacements
import schedule
import hybrid
import logging
import os
import sys
import subprocess
import psycopg2

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update, job_queue, chat_data):
    update.message.reply_text(
        'Добро пожаловать!\n'
        'По умолчанию установлена группа пр1-15, для изменения \
        введите комманду /group\n'
        'Для получения информации введите /help\n'
        'Для получения комманд введите /command')
    regUser(update.effective_user.id, update.effective_user.username)


def dbQuery(query, *args):
    result = None
    try:
        parse.uses_netloc.append("postgres")
        dataurl = os.environ.get('DATABASE_URL')
        url = parse.urlparse(dataurl)
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port)
        cur = conn.cursor()
        cur.execute(query, args)
        try:
            result = cur.fetchall()
        except Exception:
            result = None
        try:
            conn.commit()
        except Exception:
            pass
    except psycopg2.ProgrammingError as e:
        print('db error')
        print(e)
        result = None
    finally:
        cur.close()
        conn.close()
        return result


def groups():
    grp = os.listdir(os.path.join('.', 'rs'))
    grp = [x.lower()[0:-4] for x in grp]
    return grp


def help(bot, update):
    update.message.reply_text(
        'Бот, присылающий ответы по предмету ТБД. \
        Также, он может прислать замены и расписание предметов ЧЭМК.\n'
        'Для получения списка и описания комманд введите /command')


def command(bot, update, args):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text(
        '/sch [день] - Расписание. \
        По умолчанию возвращает расписание на завтра.\n'
        'Принимает один необязательный аргумент.\n'
        '[день] = \'пн\',\'вт\',\'ср\',\'чт\',\'пт\'\
        ,\'сб\',\'завтра\',\'сегодня\'\n'
        '\n/rep [день] [группа] - Замены. \
        По умолчанию возвращает замены группы на завтра.\n'
        'Принимет два необязательных аргумента в любой последовательности.\n'
        '[день] = \'сегодня\', \'завтра\'\n'
        '[группа] = Группы ЧЭМК\n'
        '\n/hyb [день] [группа] - Расписание с заменами. \
        По умолчанию возвращает расписание группы на завтра\n'
        'Принимает два необязательных аргумента в любой последовательности.\n'
        '[день] = \'сегодня\', \'завтра\'\n'
        '[группа] = Группы ЧЭМК.')


def regUser(userid, username):
    here = dbQuery("SELECT id FROM users")
    newHere = []
    for i in range(0, len(here)):
        newHere.insert(0, here[i][0])
    here = newHere
    retAn = 'tbd'
    grp = 'пр1-15'
    try:
        if userid not in here:
            dbQuery(
                "INSERT INTO users (id, name, note, ret, grp) \
                VALUES (%s, %s, 0, %s, %s)",
                userid, username, retAn, grp)
    except IndexError:
        dbQuery(
            "INSERT INTO users (id, name, note, ret, grp) \
            VALUES (%s, %s, 0, %s, %s)",
            userid, username, retAn, grp)


def sch(bot, update, args):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    chat_id = update.message.chat_id
    gr = dbQuery("SELECT grp FROM users WHERE id = %s", chat_id)[0][0]
    day = "завтра"
    if len(args) == 1:
        if args[0].lower in groups():
            gr = args[0].lower()
        else:
            day = args[0].lower()
    elif len(args) == 2:
        if args[0].lower in groups():
            gr = args[0].lower()
            day = args[1].lower()
        else:
            day = args[0].lower()
            gr = args[1].lower()

    update.message.reply_text(schedule.getSchedule(gr, day))


def hyb(bot, update, args):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    chat_id = update.message.chat_id
    gr = dbQuery("SELECT grp FROM users WHERE id = %s", chat_id)[0][0]
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
    update.message.reply_text(hybrid.getHybrid(gr, time))


def rep(bot, update, args):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    chat_id = update.message.chat_id
    gr = dbQuery("SELECT grp FROM users WHERE id = %s", chat_id)[0][0]
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
    update.message.reply_text(replacements.getChange(gr, time))


def echo(bot, update):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    ans = answers.getAnswer(update.message.text)
    for i in range(0, len(ans), 2):
        update.message.reply_text(ans[i] + ans[i + 1])
        if i > 10:
            update.message.reply_text(
                "Очень много ответов. Задайте более точный вопрос.")
            break
    if len(ans) == 0:
        update.message.reply_text("Вопрос не найден.")


def settings(bot, update):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text("/group - Выбор группы\n"
                              "/set - Установка таймера\n"
                              "/unset - Удаление таймера\n"
                              "/ans - Возвращаемый ответ")


def group(bot, update, args):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    chat_id = update.message.chat_id
    if (len(args) != 1):
        update.message.reply_text("Некорректное количестов аргументов.")
        return
    group = args[0].lower()
    if group not in groups():
        update.message.reply_text("Некорректная группа.")
    else:
        dbQuery("UPDATE users SET grp = %s WHERE id = %s", group, chat_id)
        update.message.reply_text("Установлена группа {}.".format(group))


def note(bot, job):
    global ss
    ids = dbQuery("SELECT id FROM users WHERE note = 1")
    for i in range(0, len(ids)):
        gr = dbQuery("SELECT grp FROM users WHERE id = %s", ids[i][0])[0][0]
        rp = replacements.getChange(gr, "завтра")
        if rp != ss[gr] and rp != "Сервер недоступен." and rp != "Нет замен." \
            and rp != "Что-то не так. Проверьте замены вручную." \
                and rp != "Расписание не готово.":
            idsGroup = dbQuery("SELECT id FROM users WHERE grp = %s", gr)
            for j in range(0, len(idsGroup)):
                bot.send_message(idsGroup[j][0], text=rp)
            ss.update({gr: rp})


def setNote(bot, update, job_queue, chat_data):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    chat_id = update.message.chat_id
    update.message.reply_text('Таймер на уведомление установлен!')
    gr = dbQuery("SELECT grp FROM users WHERE id = %s", chat_id)[0][0]
    ss.update({gr: replacements.getChange(gr, 'завтра')})
    dbQuery("UPDATE users SET note = 1 WHERE id = %s", chat_id)


def unsetNote(bot, update, chat_data):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    chat_id = update.message.chat_id
    dbQuery("UPDATE users SET note = 0 WHERE id = %s", chat_id)
    update.message.reply_text('Таймер удалён!')


def ans(bot, update, args):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    rets = ['tbd', 'pp']
    if (len(args) != 1):
        update.message.reply_text('Некорректноек количество аргументов.')
        return
    if (args[0] not in rets):
        update.message.reply_text(
            'Некорректный аргумент. Допустимые варианты: {}'.format(
                ', '.join(rets)))
        return
    chat_id = update.message.chat_id
    dbQuery("UPDATE users SET ret = %s WHERE id = %s", args[0], chat_id)
    update.message.reply_text('Возвращаемый ответ обновлён!')


def info(bot, update):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    chat_id = update.message.chat_id
    smth = dbQuery("SELECT * from users where id = %s", (chat_id))
    for col in smth:
        timers = {0: 'Не установлен', 1: 'Установлен'}
        retAns = {'tbd': 'ТБД', 'pp': 'Прикладное программирование'}
        ret = "Номер пользователя: {}\nTelegram ID: {}\nСтатус таймера: {}" \
            "\nВозвращаемый ответ: {}\nГруппа: {}".format(
                col[0], col[1], timers[col[3]], retAns[col[4]], col[5])
        update.message.reply_text(ret)


def check(bot, update):
    global ss
    print(ss)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def onStart(bot, chat_data, job_queue):
    jobId = dbQuery("SELECT id FROM users WHERE id = 451884661")
    print(jobId[0][0])
    global ss
    ss = {}
    for i in groups():
        ss.update({i: replacements.getChange(i, "завтра")})
    try:
        job = job_queue.run_repeating(note, interval=60, context=jobId[0][0])
        chat_data[jobId[0][0]
                  if jobId[0][0] not in chat_data else None]['job'] = job
    except Exception as e:
        print(e)
    print("BOT STARTED!")


def main():
    TOKEN = os.environ.get('TOKEN')
    updater = Updater(TOKEN)
    bt = Bot(TOKEN)
    dp = updater.dispatcher
    onStart(bt, dp.chat_data, dp.job_queue)
    dp.add_handler(
        CommandHandler(
            "start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rep", rep, pass_args=True))
    dp.add_handler(CommandHandler("settings", settings))
    dp.add_handler(CommandHandler("group", group, pass_args=True))
    dp.add_handler(CommandHandler("sch", sch, pass_args=True))
    dp.add_handler(CommandHandler("hyb", hyb, pass_args=True))
    dp.add_handler(CommandHandler("command", command, pass_args=True))
    dp.add_handler(
        CommandHandler(
            "set", setNote, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unsetNote, pass_chat_data=True))
    dp.add_handler(CommandHandler("ans", ans, pass_args=True))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("check", check))

    def stop_and_restart():
        updater.stop()
        subprocess.call(
            ["python", os.path.join(sys.path[0], __file__)] + sys.argv[1:])

    def restart(bot, update):
        update.message.reply_text('Бот перезапускается...')
        Thread(target=stop_and_restart).start()

    dp.add_handler(
        CommandHandler(
            'rs', restart, filters=Filters.user(username='@Dmatrix')))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
