activity_dic = {'none': 0, 'online': 1, 'offline': 2, 'error': 3}


def activity_to_int(act):
    global activity_dic

    res = activity_dic.get(act)

    if res is None:
        return 4
    return res
