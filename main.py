import logging
import logging.config
import os
import re
import time
from datetime import datetime as dt

import requests
from pyppeteer import launch
from telethon import TelegramClient, events

from settings import API_ID, API_HASH, BOT_TOKEN, WIDTH, HEIGHT, DIRECTORY_PATH
from settings import log_config

logging.config.dictConfig(log_config)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

browser, webpage = None, None

os.makedirs(os.path.dirname(DIRECTORY_PATH), exist_ok=True)


def get_urls(string):
    regex = r"(?:(?:https?)?(?:\:\/\/)?)[a-zA-Z0-9\.\/\?@\-_=#]+\.(?:[a-zA-Z]){2,6}(?:[a-zA-Z0-9\.\&\/\?\:@\-_=#%])*"
    return re.findall(regex, string)


def file_name(url):
    u_start = (re.match(r'http(s)?(:)?(\/\/)?(www\.)?', url)).end()
    u_clean = url[u_start:]
    chars = '//\\.'
    for c in chars:
        u_clean = u_clean.replace(c, '_')
    return f'{dt.now().strftime("%Y-%m-%d_%H:%m")}_{u_clean}.jpg'


async def start_browser():
    global browser, webpage
    browser = await launch(headless=True, args=['--no-sandbox'])
    webpage = await browser.newPage()
    await webpage.setViewport({'width': WIDTH, 'height': HEIGHT})


@bot.on(events.NewMessage(pattern='/start'))
async def start_bot(event):
    await event.respond('Отправь мне ссылку для получения скриншота страницы :)')
    raise events.StopPropagation


@bot.on(events.NewMessage(outgoing=False))
async def echo(event):
    try:
        urls = get_urls(event.text)
        for url in urls:
            logging.info(url)
            await event.respond(f'Статус ответа страницы: {requests.get(url).status_code}')
            await webpage.goto(url)
            await webpage.screenshot(path=f'{DIRECTORY_PATH}/{file_name(url)}', fullPage=False)
            await event.reply(file=f'{DIRECTORY_PATH}/{file_name(url)}')


    except Exception as er:
        await event.reply(event.text)
        await event.respond(str(er)[:3000])
        logging.exception(er)
        return


if __name__ == '__main__':
    with bot:
        bot.loop.run_until_complete(start_browser())
        bot.run_until_disconnected()
