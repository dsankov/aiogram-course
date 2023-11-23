
import os
from environs import Env
from rich import print as rprint







env: Env = Env()
env.read_env()

rprint(env('BOT_TOKEN') )
rprint(os.getenv('BOT_TOKEN'))