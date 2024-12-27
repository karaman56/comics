import os
import telebot
import requests
from dotenv import load_dotenv
import random

MAX_COMIC_NUMBER = 3028

def generate_comic_url():
    random_number = random.randint(1, MAX_COMIC_NUMBER)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    return url


def get_comic_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def create_comic_folder(folder_name='comics'):
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


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


def clean_up(file_path):
    os.remove(file_path)


def send_comic(bot, telegram_channel_id):
    url = generate_comic_url()
    comic_data = get_comic_data(url)

    comic_image_url = comic_data.get('img')
    comic_image_title = comic_data.get('title')
    comic_image_alt = comic_data.get('alt')

    comic_folder = create_comic_folder()
    comic_file_path = os.path.join(comic_folder, f"{comic_image_title}.png")

    try:
        download_comic(comic_image_url, comic_file_path)
        send_comic_message(bot, telegram_channel_id, comic_image_title, comic_file_path, comic_image_alt)
    finally:
        if os.path.exists(comic_file_path):
            clean_up(comic_file_path)


def print_message(message):
    print(message)


def run_bot():
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    bot = telebot.TeleBot(token)

    print_message("Бот запущен. Публикуем комикс...")
    send_comic(bot, telegram_channel_id)
    print_message("Комикс опубликован. Скрипт завершает работу.")

if __name__ == "__main__":
    run_bot()







