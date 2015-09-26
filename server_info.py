from datetime import datetime
import os

server_start_time = datetime.now()
processed_telegram_messages = 0
bd_saves = 0


def get_uptime() -> str:
    cur = datetime.now()

    dif = cur - server_start_time

    return 'uptime ' + str(dif) \
            + os.linesep + 'processed telegram messages ' + str(processed_telegram_messages) \
            + os.linesep + 'bd saves ' + str(bd_saves) \
            + os.linesep + 'version 0.7.1'
