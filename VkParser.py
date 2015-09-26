import requests
import vk
import activity_helper
from vk_user import vk_user
from datetime import datetime
import time
import VkList


vk_access_token=''


def getUserId(link, api):
    id = link
    if 'vk.com/' in link:
        id = link.split('/')[-1]
    if not id.replace('id', '').isdigit():
        time.sleep(1)
        id = api.utils.resolveScreenName(screen_name=id)['object_id']
    else:
        id = id.replace('id', '')
    return int(id)


def set_id_if_needed(user: vk_user, vkapi) -> int:
    id = 0
    if user.id > 0:
        id = user.id
    else:
        id = getUserId(user.url, vkapi)
        user.id = id
    return id


def process(users):
    global vk_access_token
    
    if vk_access_token=='':
        f = open('vk_api.txt')
        vk_access_token=f.readlines()[0]
        f.close()
    
    vkapi = vk.API(access_token=vk_access_token)

    cur = datetime.now()
    index = cur.hour * 60 + cur.minute

    ids = []

    for user in users:
        ids.append(set_id_if_needed(user, vkapi))

    time.sleep(1)
    results = vkapi.users.get(user_ids=','.join(map(str, ids)), fields='online')

    for i in range(len(results)):
        res = results[i]
        user = VkList.get_user_by_id(res['id'])
        if user is None:
            continue

        online = 'offline'
        if res['online'] == 1:
            online = 'online'

        user.times[index] = activity_helper.activity_to_int(online)
        user.name = res['first_name'] + ' ' + res['last_name']



