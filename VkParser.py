import requests
import activity_helper
from vk_user import vk_user
from datetime import datetime
import time
import VkList

vk_access_token = ''


METHODS_URL = 'https://api.vk.com/method/'


def getUserId(link):
    id = link
    if 'vk.com/' in link:
        id = link.split('/')[-1]
    if not id.replace('id', '').isdigit():
        time.sleep(1)
        return requests.get(METHODS_URL + 'utils.resolveScreenName', {'screen_name': id}).json()['response'][
            'object_id']
    else:
        id = id.replace('id', '')
    return int(id)


def set_id_if_needed(user: vk_user) -> int:
    id = 0
    if user.id > 0:
        id = user.id
    else:
        id = getUserId(user.url)
        user.id = id
    return id


def process(users):
    global vk_access_token

    cur = datetime.now()
    index = cur.hour * 60 + cur.minute

    ids = []

    for user in users:
        id = set_id_if_needed(user)
        if id > 0:
            ids.append(id)

    ids_str = ','.join(map(str, ids))

    time.sleep(1)

    results = requests.get(METHODS_URL + 'users.get', {'user_ids': ids_str, 'fields': 'online'}).json()['response']

    for i in range(len(results)):
        res = results[i]
        user = VkList.get_user_by_id(res['uid'])
        if user is None:
            continue

        online = 'offline'
        if res['online'] == 1:
            online = 'online'

        user.times[index] = activity_helper.activity_to_int(online)
        user.name = res['first_name'] + ' ' + res['last_name']
