import os

import requests

from timeout_helper import timeout_helper
import VkList
import VkSpy
import server_info

URL = 'https://api.telegram.org/bot'
TOKEN = ''
offset = 0

author_id = 97397688

process_timeout = timeout_helper(1)


def init(owner_id, telegram_api_token):
    global author_id, TOKEN
    author_id = owner_id
    TOKEN = telegram_api_token


def process():
    if not process_timeout.will_process():
        return

    global offset, TOKEN

    try:
        data = {'offset': offset, 'limit': 100, 'timeout': 0}
        request = requests.post(URL + TOKEN + '/getUpdates', data=data)

        if not request.status_code == 200:
            print('telegram request code != 200')
            return

        for update in request.json()['result']:

            mes = update['message']
            from_id = mes['chat']['id']
            server_info.processed_telegram_messages += 1

            if from_id != author_id:
                send_text(from_id, 'you are not my owner')
                continue

            if not 'message' in update or not 'text' in update['message']:
                continue

            run_command(from_id, update['message']['text'])
            offset = update['update_id'] + 1
    except Exception as e:
        print('UNKNOWN EXC - ' + str(e))
        return


def run_command(chat_id, text):
    try:
        params = text
        params = params.replace('_', ' ')
        params = params.split(' ')
        params[0] = params[0].replace('/', '')

        tmp = []
        for t in params:
            tmp.append(t.lower())

        params = tmp;

        params_lens = len(params)

        if params_lens >= 1 and params[0] == 'vk':
            if params_lens >= 3:
                if params[1] == 'add':
                    VkList.add_user(params[2])
                    return
                if params[1] == 'image':

                    if params_lens >= 4:
                        try:
                            date_str = params[3].split('-')
                            # todo
                        except:
                            send_text(chat_id, 'error date processing')
                            return

                    users = VkList.get_users()
                    if params[2] == 'all':
                        for user in users:
                            img = VkSpy.get_image(user)

                            tmp = 'tmp.jpeg'

                            img.save(tmp, 'JPEG')
                            send_image(chat_id, tmp)
                        return

                    index = int(params[2])

                    users = VkList.get_users()

                    if len(users) <= index:
                        send_text(chat_id, 'out of range')
                        return

                    img = VkSpy.get_image(users[index])

                    tmp = 'tmp.jpeg'

                    img.save(tmp, 'JPEG')
                    send_image(chat_id, tmp)

                    return
            if params_lens >= 2:
                if params[1] == 'list':
                    users = VkList.get_users()
                    us = []
                    for u in range(0, len(users)):
                        us.append(str(u) + ' - ' + str(users[u].url) + ' - ' + users[u].name)
                    sep = os.linesep
                    res = sep.join(us)
                    send_text(chat_id, res)
                    return

        if params_lens >= 1 and params[0] == 'status':
            send_text(chat_id, server_info.get_uptime())
            return

        if params_lens >= 2 and params[0] == 'force' and params[1] == 'save':
            if VkSpy.save(True):
                send_text(chat_id, 'save forced ok')
            else:
                send_text(chat_id, 'save forced error')
            return
        if params_lens >= 2 and params[0] == 'force' and params[1] == 'process':
            VkSpy.process(True)
            send_text(chat_id, 'process forced')
            return

        send_text(chat_id, 'unknown command')

    except Exception as e:
        send_text(chat_id, 'error command processing - ' + str(e))


def send_image(chat_id, image_path):
    data = {'chat_id': chat_id}
    files = {'photo': (image_path, open(image_path, "rb"))}
    requests.post(URL + TOKEN + '/sendPhoto', data=data, files=files)

    return


def send_text(chat_id, text):
    data = {'chat_id': chat_id, 'text': text}
    rec = requests.post(URL + TOKEN + '/sendMessage', data=data)

    if not rec.status_code == 200:
        print("send_text error, status code - " + str(rec.status_code))
    else:
        if not rec.json()['ok']:
            print("fail json parse")
