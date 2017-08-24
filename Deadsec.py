import vk_api, random, time, config, dead
from vk_api.longpoll import VkLongPoll, VkEventType
vk = vk_api.VkApi(config.login, config.password)
vk.auth()
#Function
def send_msg (Conf, msg):
    vk.method('messages.send', {'chat_id': Conf, 'message': str(msg)})

def send_hentai_in_conf (Conf):
    hentai_storage = dead.hentai_storage
    random_hentai_number = random.randint(1, len(hentai_storage))
    vk.method('messages.send', {'chat_id': Conf, 'attachment': hentai_storage[random_hentai_number]})

def send_post (Owner):
    vk.method('wall.post', {'owner_id': Owner, 'attachment': 'photo129244038_277151715'})
def send_hentai_in_user (User):
    hentai_storage = dead.hentai_storage
    random_hentai_number = random.randint(1, len(hentai_storage))
    vk.method('messages.send', {'user_id': User, 'attachment': hentai_storage[random_hentai_number]})


#LONGPOLL

LongPoll = VkLongPoll(vk)
for event in LongPoll.listen():
    print(event.user_id)
    session = event.chat_id
    user = event.user_id
    if event.text != None and event.text.startswith('/hentai'):
        send_hentai_in_conf(int(session))
    if event.text != None and event.text.startswith('/оппозиция'):
        send_post(user)
    if event.text != None and event.text.startswith('/hentai'):
        send_hentai_in_user(user)





