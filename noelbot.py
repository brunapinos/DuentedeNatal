from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)


# class DuenteBot():
#     def __init__(self, *args, **kwargs):
#         super(VoteCounter, self).__init__(*args, **kwargs)

#         global votes
#         if self.id in votes:
#             self._ballot_box, self._keyboard_msg_ident, self._expired_event, self._member_count = votes[self.id]
#             self._editor = telepot.aio.helper.Editor(self.bot, self._keyboard_msg_ident) if self._keyboard_msg_ident else None
#         else:
#             self._ballot_box = None
#             self._keyboard_msg_ident = None
#             self._editor = None
#             self._expired_event = None
#             self._member_count = None
users = []

def start(bot, update):
    # user_name = bot.username()
    # teste = CallbackQuery
    markup = InlineKeyboardMarkup(inline_keyboard=[[
                       InlineKeyboardButton(text='Join', callback_data='teste'),
                   ]])
    bot.send_message(chat_id=update.message.chat_id, 
        text="Vamos participar do Amigo Oculto", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
   data = query.data
   if data == 'teste':
       print('oi')
    #    get_ex_callback(query)    
    # # if updater.callback_query.data == 'teste':
    # bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
    #                             text="Testes")




def close(bot, update):
    # user_name = bot.username()
    bot.send_message(chat_id=update.message.chat_id, 
        text="The sorting can start")

def gifts(bot, update):
    # user_name = bot.username()
    bot.send_message(chat_id=update.message.chat_id, 
        text="Tell me your gift")

def sort(bot, update): 
        # user_name = bot.username()
    bot.send_message(chat_id=update.message.chat_id, 
        text="Sorting")

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    # updater = Updater("745025232:AAF5j2aCdiRl2kJBtf9mEUzSPVEzsfSlkyM")
    updater = Updater("678582209:AAGdYnxxV3SkRKzWm8BBR8ur4ozAcozzxQo")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("gifts", gifts))
    dp.add_handler(CommandHandler("sort", sort))
    # dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    # j = updater.job_queue
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
