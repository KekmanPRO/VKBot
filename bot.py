# -*- coding: utf-8 -*-

import vk_api
import time
import random
import time
from threading import Timer
from vk_api.longpoll import VkLongPoll, VkEventType
import sys  

import config
import data
import emoji

reload(sys)  
sys.setdefaultencoding('utf8')

api = None
api = vk_api.VkApi(config.username, config.password)
try:
    api.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)



def randomEmojiString():
    result = ''
    len = random.randint(1,7)
    for i in range(len):
        result += emoji.random_emoji()[0]
    return result

def getRandomPhoto(albumName):
    albums = api.method('photos.getAlbums', {})
    for album in albums['items']:
        if album['title'] == albumName:
            albumId = album['id']
            params = {'album_id': albumId}
            photos = api.method('photos.get', params)

            photo = random.choice(photos['items'])

            photoId = 'photo' + str(photo['owner_id']) + '_' + str(photo['id'])
            return photoId
        else:
            print('Album \"' + albumName + '\" not found!')
            return 'error'

def respond(to, values):
    if 'chat_id' in to:
        values['chat_id'] = to['chat_id']
        api.method('messages.send', values)
    else:
        values['user_id'] = to['user_id']
        api.method('messages.send', values)

timer = None

def sendMessageWithText(chat_id, text):
    print ("sendMessageWithText: " + text)
    respond({'chat_id': chat_id}, {'message': text + u" " + random.choice(data.words)})

def sendMessage(chat_id):
    global timer

    print ("sendMessage: " + chat_id)

    photoId = None
    stickerId = None
    responce = random.choice(data.words)

    if random.randint(0,1) == 1:
        responce = random.choice(data.phrases)
    elif random.randint(0,1) == 1:
        responce = randomEmojiString()
    elif random.randint(0,1) == 1:
        photoId = getRandomPhoto("BOT")
    elif random.randint(0,1) == 1:
        stickerId = random.randint(1,168)

    values = {'message': responce}
    if stickerId is not None:
        values['sticker_id'] = stickerId
    if photoId is not None:
        values['attachment'] = photoId

    respond({'chat_id': chat_id}, values)
    timer = Timer(10, lambda: sendMessage(chat_id) )
    timer.start()

def processCommand(command):
    global timer

    print ("processCommand: " + command)
    if command.startswith('/start'):
        groupName = command.split("/start", 1)[1].strip()
        print ('starting at ' + groupName)
        dialogs = api.method('messages.getDialogs')
        print(dialogs)
        for item in dialogs['items']:
            print (item)
            if 'title' in item['message'] and item['message']['title'] == groupName:
                sendMessage(item['message']['chat_id'])
                return
        print('No groups found for: ' + groupName)
    elif command.startswith('/stop'):
        timer.cancel()
        timer = None

def receivedMessageFromChat(chat_id, user_id, text):
    global timer

    print ("receivedMessageFromChat: " + user_id + " " + text)
    if user_id == '124157748':
        print ("receivedMessageFromChat!!!!!!!!!!! ")
        if text.startswith('noize'):
            sendMessage(str(chat_id))
        elif text.startswith('stop'):
            timer.cancel()
            timer = None
        else:
            print("unhandled command: " + text)
    elif timer is not None:
        sendMessageWithText(chat_id, text)


longpoll = VkLongPoll(api)
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        print('New message:')

        if event.from_me:
            print('FROM ME: ')
        elif event.to_me:
            print('TO ME: ')

        if event.from_user:
            print('event.from_user: ' + str(event.user_id))
            if event.user_id == 124157748 and event.text.startswith('/'): 
                processCommand(event.text)
            else:
                sendMessageWithText(event.user_id, event.text)
        elif event.from_chat:
            print(event.user_id, 'in chat', event.chat_id)
            if event.to_me:
                receivedMessageFromChat(event.chat_id, event.user_id, event.text)
        elif event.from_group:
            print('group', event.group_id)

        print('Text: ', event.text)
        print(event.type, event.raw[1:])
        print()
"""
    elif event.type == VkEventType.USER_TYPING:
        print('Печатает ')

        if event.from_user:
            print(event.user_id)
        elif event.from_group:
            print('администратор группы', event.group_id)

    elif event.type == VkEventType.USER_TYPING_IN_CHAT:
        print('Печатает ', event.user_id, 'в беседе', event.chat_id)

    elif event.type == VkEventType.USER_ONLINE:
        print('Пользователь', event.user_id, 'онлайн', event.platform)

    elif event.type == VkEventType.USER_OFFLINE:
        print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

    else:
        print(event.type, event.raw[1:])
"""
