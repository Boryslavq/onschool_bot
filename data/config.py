from environs import Env
import os

_path = os.path.abspath(os.curdir)
env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
YOO_TOKEN = env.str('YOO_TOKEN')
QIWI_TOKEN = env.str('QIWI_TOKEN')

sqlite_uri = rf'sqlite:///{_path}\Resources\customer.sqlite'
