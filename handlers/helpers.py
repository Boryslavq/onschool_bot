from re import sub

from yoomoney import Client
from data import config


async def check_num(_str):
    norm_mob = sub(r'(\s+)?[+]?[-]?', '', _str)
    if norm_mob.isdigit() and len(norm_mob) > 7:
        return int(norm_mob)
    else:
        return False


async def check(bill_id: str):
    client = Client(config.YOO_TOKEN)
    history = client.operation_history(label=bill_id).operations
    if len(history) > 0:
        return history[0].status == 'success'
    return False
