import time
import VkSpy
import telegram_bot
import json


def set_up() -> str:
    try:
        dic = json.load(open("config.txt"))

        telegram_bot.init(dic['telegram_owner_id'], dic['telegram_api_token'])

        return ''
    except Exception as e:
        return 'error - ' + str(e)


if __name__ == "__main__":

    res = set_up()

    if res == '':
        print('server started')
        while True:
            telegram_bot.process()
            VkSpy.process()
            time.sleep(1)
    else:
        print(res)
