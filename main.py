import telebot
import time
from threading import Thread
import schedule

import requests
from bs4 import BeautifulSoup
from telebot import types

HEADERS = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

file = open('users.txt', 'r').readlines()

users = {}
for line in file:
	spl = line .split(':')
	users[int(spl[0])] = spl[1].replace('\n', '')

bot = telebot.TeleBot('1938325222:AAH233hjN2GDDoHdYlhSXyCBm0UNC_z5MTw')

def save():
	mas = []
	for key in users:
		string = str(key) + ':' + users[key]
		mas.append(string)
	open('users.txt', 'w', errors = 'ignore').write('\n'.join())

def shedule_checker():
	while True:
		schedule.run_pending()
		time.sleep(1)

@bot.message_handler(commands = ['start', 'change'])
def start(message):
	bot.reply_to(message, 'Привет дружище! Отправь мне название криптовалюты)\nbitcoin\nethereum\ncardano\nbinance coin\ntether\nsolana\nxrp\ndogecoin\nusd coin\npolkadot')
	bot.reply_to(message, 'Вот все мои команды:\nchange')
	bot.register_next_step_handler_by_chat_id(message.chat.id, start2)

def start2(message):
	users[message.chat.id] = message.text.lower()
	bot.reply_to(message, 'Окей) Спасибо 0_0')
	save()

def SPAM():
	for key in users:
		content = requests.get('https://ru.investing.com/crypto/{}'.format(users[key].replace(' ', '-')), headers = HEADERS).content
		soup = BeautifulSoup(content, 'html.parser')
		change = soup.findAll('span', 'parentheses')[0].text.replace(',', '.')

		if change[0] == '-':
			if float(change[1:-1]) > 4:
				bot.send_message(key, 'Цена вашк=ей криптовалюты за сутки упала на ' + change[1:])
			else:
				bot.send_message(key, 'Крипта спит... Ваши денюжки в безопасности :)')
		else:
			if float(change[:-1]) > 4:
				bot.send_message(key, 'Цена вашк=ей криптовалюты за сутки упала на ' + change[1:])
			else:
				bot.send_message(key, 'Крипта спит... Ваши денюжки в безопасности :)')

schedule.every().day.at("19:04").do(SPAM)
Thread(target = shedule_checker).start()

bot.polling(none_stop = True)