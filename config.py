import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_dropbox_access_token():
    return os.environ.get("sl.BRzn7if2jRs-o9Okm1qWAa6nJ17Ux88cbVb8aO6feEzfJuGhfpA42NzHM-_avWMgHfe2_1YcHQMAcsFjHyHRE5GhuDTAtg7QUOzu7fvGQT6stq3E_G7aBF6ycIoYUlYZASIQBeAxZeE", "h9r209copjs6qtt")
