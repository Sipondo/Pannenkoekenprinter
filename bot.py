import os
import telebot
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

with open("token") as file:
    TOKEN =file.readline()[:-1]
bot = telebot.TeleBot(TOKEN)

print("lel")
#
# #commands=['start', 'help']
# @bot.message_handler()
# def send_welcome(message):
#     bot.reply_to(message, u"Sentiment score: ")

def read_params():
    with open("params") as file:
        return [int(x[:-1]) for x in file]

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document','photo'])
def handle_image(message):
    # print("wow")
    # print(message.document)
    if (message.document):
        document = message.document
    else:
        document = message.photo[0]
    photo_url = "https://api.telegram.org/file/bot{0}/{1}".format(TOKEN, bot.get_file(document.file_id).file_path)
    response = requests.get(photo_url)
    img = Image.open(BytesIO(response.content))
    img.save("buffer.jpg")
    bot.send_message(message.chat.id, "Image received!")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "help, show, params, size, blurred, equalized, cwhite, inverted")

@bot.message_handler(commands=['show'])
def handle_return(message):
    img = open("buffer.jpg", 'rb')
    bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=['params'])
def handle_params(message):
    bot.send_message(message.chat.id, [str(x) for x in read_params()])

@bot.message_handler(commands=['size'])
def handle_set_size(message):
    param_value = int(message.text[6:])
    if(param_value<50):
        param_value = 50
    bot.send_message(message.chat.id, [str(x) for x in read_params()])


bot.polling()
