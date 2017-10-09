from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent
import logging, answers, replacements, schedule, os, hybrid

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


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

def sch(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    day = "завтра"
    if len(args) == 1:
        day = args[0].lower()
    update.message.reply_text(schedule.getSchedule(day))

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
    
def echo(bot, update):
    #update.message.reply_text(update.message.text)
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


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = "462202131:AAETYcmO8qi2m1SaQzs-zzqC_ycRHOqXG14"
    #PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rep", rep, pass_args=True))
    dp.add_handler(CommandHandler("sch", sch, pass_args=True))
    dp.add_handler(CommandHandler("hyb", hyb, pass_args=True))
    dp.add_handler(CommandHandler("command", command, pass_args=True))
    # on noncommand
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot

    updater.start_polling()
    #WEBHOOK HEROKU
    #updater.start_webhook(listen="0.0.0.0", port = PORT, url_path = TOKEN)
    #APPNAME = "telegrambotchemk"
    #updater.bot.set_webhook("https://{}.herokuapp.com/".format(APPNAME) + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
