import os
import telebot
import requests
from dotenv import load_dotenv
import random

MAX_COMIC_NUMBER = 3028


def get_random_comic_data():
    """Возвращает данные о случайном комиксе."""
    random_number = random.randint(1, MAX_COMIC_NUMBER)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def prepare_comic_file_path(comic_image_title):
    """Подготавливает путь для сохранения комикса."""
    comic_folder = 'comics'
    os.makedirs(comic_folder, exist_ok=True)
    return os.path.join(comic_folder, f"{comic_image_title}.png")


def download_comic(comic_image_url, save_path):
    """Скачивает комикс по URL и сохраняет его по указанному пути, возвращая путь к файлу."""
    response = requests.get(comic_image_url, stream=True)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)
    return save_path


def send_comic(bot, telegram_channel_id, comic_image_title, comic_file_path, comic_image_alt):
    """Отправляет комикс в Telegram."""
    bot.send_message(chat_id=telegram_channel_id, text=comic_image_title)
    with open(comic_file_path, 'rb') as photo:
        bot.send_photo(chat_id=telegram_channel_id, photo=photo)
    bot.send_message(chat_id=telegram_channel_id, text=comic_image_alt)


def fetch_comic_data():
    """Получает данные о комиксе и возвращает заголовок, URL изображения и текст комментария."""
    comic_data = get_random_comic_data()
    comic_image_title = comic_data.get('title')
    comic_image_url = comic_data.get('img')
    comic_image_alt = comic_data.get('alt')
    return comic_image_title, comic_image_url, comic_image_alt


def run_bot():
    """Запускает бота и отправляет комикс."""
    load_dotenv()
    try:
        token = os.environ['TELEGRAM_BOT_TOKEN']
        telegram_channel_id = os.environ['TELEGRAM_CHANNEL_ID']
    except KeyError as e:
        raise RuntimeError(f"Переменная окружения не установлена: {e}")

    bot = telebot.TeleBot(token)

    print("Бот запущен.")

    comic_image_title, comic_image_url, comic_image_alt = fetch_comic_data()
    comic_file_path = prepare_comic_file_path(comic_image_title)

    try:
        download_comic(comic_image_url, comic_file_path)
        send_comic(bot, telegram_channel_id, comic_image_title, comic_file_path, comic_image_alt)
    finally:
        if os.path.exists(comic_file_path):
            try:
                os.remove(comic_file_path)
                print(f"Временный файл {comic_file_path} удален.")
            except Exception as e:
                print(f"Ошибка при удалении файла: {e}")

    print("Комикс опубликован.")


if __name__ == "__main__":
    run_bot()
















