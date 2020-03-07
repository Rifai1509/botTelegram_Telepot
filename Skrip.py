import sys
import time
import random
import datetime
import telepot

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print ('Got command: %s' % command)
    if command == '/start':
        bot.sendMessage(chat_id, text = '''
halo, 
silakan pilih:
1. /aaa
2. /bbb
''')
    elif command == '/aaa':
        bot.sendMessage(chat_id, text = '''anda telah milih aaa
/kembali''')
    elif command == '/bbb':
        bot.sendMessage(chat_id, text = '''anda telah milih bbb
        /kembali''')
    elif command == '/kembali':
        bot.sendMessage(chat_id, text = '''halo,
Anda telah pilih kembali''')
bot = telepot.Bot('isikan Token Api disini')
bot.message_loop(handle)
while 1:
    time.sleep(10)