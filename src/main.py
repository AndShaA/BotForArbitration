import config
import telebot

from src.bot_logic import BotLogic

bot = telebot.TeleBot(config.TOKEN)
logic = BotLogic()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я анализирую пары на бирже YoBit и помогаю в арбитражном трейдинге. '
                                      'Для начала анализа напиши /analysis')
@bot.message_handler(commands=['analysis'])
def analysis(message):
    bot.send_message(message.chat.id, 'Идет анализ')
    best_pair = logic.search_best_trade()
    answer = ''
    for pair in best_pair:
        answer += str(pair) + ': +' + str(best_pair[pair]) + '%\n'
    bot.send_message(message.chat.id, answer)



if __name__ == '__main__':
     bot.infinity_polling()