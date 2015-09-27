import os
from vk_user import vk_user

loaded = False
users = []

vk_user_file = "vk_list.txt"


def get_users():
    global users, loaded

    if loaded:
        return users

    try:
        f = open(vk_user_file, 'r')
        users.clear()
        for line in f.readlines():
            user = line.replace('\n', "").replace('\r', "")
            if user == '':
                continue
            some = vk_user(user)
            users.append(some)
        f.close()
        loaded = True
        return users
    except Exception as e:
        print('vk_list error - '+str(e))
        return []


def get_user_by_id(id: int) -> vk_user:
    for user in users:
        if user.id == id:
            return user
    return None


def add_user(url):
    global loaded, users
    loaded = True

    users = get_users()
    users.append(vk_user(url))

    f = open(vk_user_file, 'w')
    for user in users:
        f.write(str(user.url) + os.linesep)
    f.close()
    return
