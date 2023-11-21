import os
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA
from Cryptodome.Signature import PKCS1_v1_5
from telebot import types
import datetime
import telebot
import main


BOT_TOKEN = open('token').read()

bot = telebot.TeleBot(BOT_TOKEN)


def red(message:str):
    ids = open('ids','r').read().split()
    for i in ids:
        bot.send_message(i,message)

def priv_red(message:str,id:int):
    bot.send_message(id,message)

def extract_arg(arg:str):
    return arg.split()[1:]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id,open('altera.png' , 'rb'))
    bot.send_message(message.chat.id,'Вас приветствует проект ALTERA! Это программа, сделанная для того, чтобы проводить открытые выборы в рамках небольшой организации, как например школа. Но этот проект особый. Мы не просто собираем ваши голоса, а потом говорим кто победил. Мы ведём статистику за время голосования, а также шифруем все голоса наших пользователей так, чтобы никто не мог их подделать. Это будет трудно провернуть даже организаторам голосования, благодаря асимметричному шифрованию, которым защищены ваши голоса./help')

@bot.message_handler(commands=['regist'])
def regist(message):
    id=message.from_user.id
    nick = extract_arg(message.text)[0]
    ans=main.regist(id=str(id),nick=nick)
    bot.send_message(id,ans)
    


@bot.message_handler(commands=['voters'])
def send_voters(message):
    main.voters()
    bot.send_document(message.chat.id,open('report'))
    bot.send_message(message.chat.id,'Это список всех проголосовавших и их голосов. Вы это можете увидеть так как это голосование открытое. Каждый может проверить систему на наличие нарушений.')
    os.remove('report')

@bot.message_handler(commands=['cands'])
def send_cands(message):
    ans =main.send_cands()
    bot.send_message(message.chat.id,ans)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '/help - вызвать помощь\n/start - приветствие\n/cands - посмотреть список кандидатов\n!vote name 0 - проголосовать, вместо name ставите выданный вам никнейм, на вместо цифры пишите номер кандидата, также к сообщению прикрепите файл с вашим личным ключом\n/results - посмотреть график результатов\n/voters - посмотреть результат голосования в виде файла с голосом каждого пользователя')

@bot.message_handler(commands=['results'])
def results(message):
    ans =main.results()
    if ans != 'Никто ещё не проголосовал':
        bot.send_photo(message.chat.id, open('graph.png', 'rb'))
    bot.send_message(message.chat.id, ans)
    

@bot.message_handler(content_types=['document'])#this command is used for uploading file with private key
def vote(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    capt=message.caption
    ans=main.vote(cap=capt,file=downloaded_file)
    if ans == 'red alert':
        red()
        breakpoint()
    capt= capt.split()
    nick=capt[1]
    main.get_id(nick)
    bot.send_message(main.get_id(nick),ans)




bot.infinity_polling()