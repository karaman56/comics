import os
import telebot
import requests
from dotenv import load_dotenv
import random



def get_telegram_bot_token():
    load_dotenv()
    return os.getenv('TELEGRAM_BOT_TOKEN')

def get_telegram_channel_id():
    load_dotenv()
    return os.getenv('TELEGRAM_CHANNEL_ID')

def create_comic_folder(folder_name='comics'):
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def create_bot(token):
    return telebot.TeleBot(token)

def generate_comic_url():
    random_number = random.randint(1, 3028)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    return url

def download_comic(comic_image_url, save_path):
    response = requests.get(comic_image_url, stream=True)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)

def send_comic(bot, telegram_channel_id):
    url = generate_comic_url()
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    comic_image_url = comic_data.get('img')
    comic_image_title = comic_data.get('title')
    comic_image_alt = comic_data.get('alt')

    comic_folder = create_comic_folder()

    comic_file_path = os.path.join(comic_folder, f"{comic_image_title}.png")

    download_comic(comic_image_url, comic_file_path)

    bot.send_message(chat_id=telegram_channel_id, text=comic_image_title)
    bot.send_photo(chat_id=telegram_channel_id, photo=open(comic_file_path, 'rb'))
    bot.send_message(chat_id=telegram_channel_id, text=comic_image_alt)

    os.remove(comic_file_path)

def run_bot():
    token = get_telegram_bot_token()
    telegram_channel_id = get_telegram_channel_id()
    bot = create_bot(token)
    print("Бот запущен. Публикуем комикс...")
    send_comic(bot, telegram_channel_id)
    print("Комикс опубликован. Скрипт завершает работу.")


if __name__ == "__main__":
    run_bot()


