from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, answers, replacements, schedule, os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')

def sch(bot, update, args):
    day = "завтра"
    if len(args) == 1:
        day = args[0].lower()
    update.message.reply_text(schedule.getSchedule(day))

def rep(bot, update, args):
    gr = "пр1-15"
    time = "tomorrow"
    if len(args) == 2:
        if args[0] == "tomorrow" or args[0] == "today":
            time = args[0]
            gr = args[1]
        else:
            time = args[1]
            gr = args[0]
    elif len(args) == 1:
        if args[0] == "tomorrow" or args[0] == "today":
            time = args[0]
        else:
            gr = args[0]
    update.message.reply_text(replacements.findChange(gr,time))
    
def echo(bot, update):
    #update.message.reply_text(update.message.text)
    update.message.reply_text(answers.getAnswer(update.message.text))

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = "462202131:AAETYcmO8qi2m1SaQzs-zzqC_ycRHOqXG14"
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rep", rep, pass_args=True))
    dp.add_handler(CommandHandler("sch", sch, pass_args=True))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot

    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port = PORT, url_path = TOKEN)
    APPNAME = "telegrambotchemk"
    updater.bot.set_webhook("https://{}.herokuapp.com/".format(APPNAME) + TOKEN)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
