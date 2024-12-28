import os
import telebot
import requests
from dotenv import load_dotenv
import random

MAX_COMIC_NUMBER = 3028

def get_comic_data():
    random_number = random.randint(1, MAX_COMIC_NUMBER)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_comic(comic_image_url, save_path):
    response = requests.get(comic_image_url, stream=True)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)


def send_comic_message(bot, telegram_channel_id, title, image_path, alt_text):
    bot.send_message(chat_id=telegram_channel_id, text=title)
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=telegram_channel_id, photo=photo)
    bot.send_message(chat_id=telegram_channel_id, text=alt_text)


def fetch_and_download_comic():
    comic_data = get_comic_data()
    comic_image_url = comic_data.get('img')
    comic_image_title = comic_data.get('title')
    comic_image_alt = comic_data.get('alt')
    comic_folder = 'comics'
    os.makedirs(comic_folder, exist_ok=True)
    comic_file_path = os.path.join(comic_folder, f"{comic_image_title}.png")

    download_comic(comic_image_url, comic_file_path)

    return comic_image_title, comic_file_path, comic_image_alt


def send_comic(bot, telegram_channel_id):
    comic_image_title, comic_file_path, comic_image_alt = fetch_and_download_comic()
    try:
        send_comic_message(bot, telegram_channel_id, comic_image_title, comic_file_path, comic_image_alt)
    finally:
        if os.path.exists(comic_file_path):
            os.remove(comic_file_path)


def run_bot():
    load_dotenv()

    try:
        token = os.environ['TELEGRAM_BOT_TOKEN']
        telegram_channel_id = os.environ['TELEGRAM_CHANNEL_ID']
    except KeyError as e:
        raise RuntimeError(f"переменная окружения не установлена: {e}")

    bot = telebot.TeleBot(token)

    print("Бот запущен.")
    send_comic(bot, telegram_channel_id)
    print("Комикс опубликован.")


if __name__ == "__main__":
    run_bot()









