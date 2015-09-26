import VkParser
import VkList
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
import PIL

from Helpers.timeout_helper import timeout_helper
import Helpers.server_info

user_directory = "users_activity"

cur_date = datetime.now()

process_timeout = timeout_helper(30)
process_save_timeout = timeout_helper(60 * 30)


def _get_file_path(file):
    return user_directory + '\\' + file + '.txt'


def _prepare_if_needed():
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)


def process(force=False):
    try:
        global user_directory, process_timeout, cur_date

        cur = datetime.now()
        users = VkList.get_users()
        if cur_date.day != cur.day:
            cur_date = cur
            for user in users:
                user.clear_times()

        if not force and not process_timeout.will_process():
            return

        _prepare_if_needed()
        VkParser.process(users)
        save()

        return
    except Exception as e:
        print('error VkSpy process'+str(e))


def get_image(user, custom_date: datetime = None) -> Image:
    try:
        _prepare_if_needed()
        f = open(_get_file_path(user.user_file), 'r')

        activity = []
        for i in range(1440):
            activity.append(0)
        cur = datetime.now()

        if not custom_date is None:
            cur = custom_date

        for line in f.readlines():
            try:
                lines = line.split(':')

                date = lines[0]

                subData = date.split('-')

                year = int(subData[0])
                month = int(subData[1])
                day = int(subData[2])

                if year == cur.year and month == cur.month and day == cur.day:
                    tmp = lines[1].split('-')
                    start_at = int(tmp[0])

                    vals = lines[2].replace('\n', '')

                    for i in range(len(vals)):
                        activity[start_at + i] = int(vals[i])

                if year >= cur.year and month >= cur.month and day > cur.day:
                    break
            except:
                continue

        img = Image.new("RGBA", (1440, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        width = img.size[0]
        height = img.size[1]

        font = ImageFont.truetype("font.ttf", 16)

        for x in range(width):
            c = int(255 * x / width)
            r = 0
            g = 0
            b = 0

            if activity[x] == 1:
                g = 255
            if activity[x] == 2:
                r = 0
                g = 0
                b = 0
            if activity[x] == 3:
                r = 255
            if activity[x] == 0:
                r = 60
                g = 60
                b = 60

            draw.line((x, 0) + (x, height), (r, g, b))

        new_width = 144 * 5
        img = img.resize((new_width, 200), PIL.Image.ANTIALIAS)

        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, new_width, 100], (0, 0, 0))
        draw.text((5, 5), user.url, (255, 255, 255), font=font)
        spyd = 1 - _get_percent(activity, 0)
        online = _get_percent(activity, 1)
        if spyd > 0:
            online /= spyd
        draw.text((5, 25), 'spyd ' + str(round(spyd * 100, 1)) + '%', (255, 255, 255), font=font)
        draw.text((5, 45), 'online ' + str(round(online * 100, 1)) + '%', (255, 255, 255), font=font)

        draw.text((100, 25), user.name, (255, 255, 255), font=font)

        for i in range(0, 24):
            x_offset = int(new_width * i / 24)
            draw.line((x_offset, 100) + (x_offset, 200), (128, 128, 128))
            draw.text((x_offset - 5, 80), str(i), (160, 160, 160), font=font)

        return img
    except:
        print('error image format')


def _get_percent(array: [], val: int):
    size = len(array)
    count = 0
    for i in range(0, size):
        if array[i] == val:
            count += 1
    return count / size


def save(force: bool = False) -> bool:
    try:
        global process_save_timeout

        if not force and not process_save_timeout.will_process():
            return

        if force:
            process_save_timeout.force_update()

        Helpers.server_info.bd_saves += 1
        users = VkList.get_users()
        for user in users:

            if not _has_any_time(user.times):
                continue

            f = open(_get_file_path(user.user_file), 'a')

            cur_time = datetime.now()

            f.write(str(cur_time.year) + '-' + str(cur_time.month) + '-' + str(cur_time.day) + ':')

            start_index = index_of_start(user.times)
            end_index = index_of_end(user.times)

            f.write(str(start_index) + '-' + str(end_index) + ':')

            if start_index >= 0 and end_index >= 0:
                for i in range(start_index, end_index + 1):
                    f.write(str(user.times[i]))
            else:
                for t in user.times:
                    f.write(str(t))
            f.write(os.linesep)
            f.close()
            user.clear_times()

        return True
    except:
        print('error vkSpy save')
        return False


def _is_new_day():
    cur = datetime.now()
    return cur.day != cur_date


def _has_any_time(times) -> bool:
    for i in range(len(times)):
        if times[i] != 0:
            return True
    return False


def index_of_start(times):
    i = 0
    while i < 1440:
        if times[i] != 0:
            return i
        i += 1

    return -1


def index_of_end(times):
    i = 1440 - 1
    while i > 0:
        if times[i] != 0:
            return i
        i -= 1

    return -1
