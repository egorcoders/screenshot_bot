import os

from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
WIDTH = int(os.getenv('WIDTH', '1920'))
HEIGHT = int(os.getenv('HEIGHT', '1080'))
DIRECTORY_PATH = os.getenv('DIRECTORY_PATH')


log_config = {
    "version": 1,
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
        "file": {
            "formatter": "std_out",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "message_logs.log"
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(levelname)s : %(module)s : %(funcName)s : %(message)s",
        }
    },
}
