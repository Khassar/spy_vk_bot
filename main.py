import time
import VkSpy
import telegram_bot


if __name__ == "__main__":
    print('server started')
    while True:

        telegram_bot.process()
        VkSpy.process()
        time.sleep(1)
