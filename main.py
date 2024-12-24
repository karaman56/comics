import os
import telebot
import requests
from dotenv import load_dotenv
import random
import schedule
import time


def create_bot():
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = telebot.TeleBot(token)
    return bot


def url_comics():
    random_number = random.randint(1, 614)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    return url


def send_comic(bot):
    telegram_chanell_id = os.getenv('TELEGRAM_CHANNEL_ID')
    url = url_comics()
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    comic_image_url = comic_data.get('img')
    comic_image_title = comic_data.get('title')
    comic_image_alt = comic_data.get('alt')

    bot.send_message(chat_id=telegram_chanell_id, text=comic_image_title)
    bot.send_photo(chat_id=telegram_chanell_id, photo=comic_image_url)
    bot.send_message(chat_id=telegram_chanell_id, text=comic_image_alt)


def job():
    bot = create_bot()
    send_comic(bot)


def main():
    print("Бот запущен.")
    schedule.every().day.at("09:00").do(job)
    schedule.every().day.at("04:16").do(job)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()

