import telebot


access_token = '299863676:AAHCDeEMvCQht5455QQRGHDEDPCJB7diHJU'
bot = telebot.TeleBot(access_token)


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
