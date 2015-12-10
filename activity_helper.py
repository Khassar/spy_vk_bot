activity_dic = {'none': 0, 'online': 1, 'online_mobile': 2, 'offline': 3, 'error': 4}


def activity_to_int(act):
    global activity_dic

    res = activity_dic.get(act)

    if res is None:
        return 4
    return res
