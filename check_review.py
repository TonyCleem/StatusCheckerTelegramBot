import requests
import time
import pprint
import os
import telegram
from dotenv import load_dotenv
from messange_sender import send_messange_via_tg_bot


def get_review_status(url, token, bot, chat_id, updates):
    text = ''
    timestamp = None
    headers = {
        'Authorization': 'Token'+' '+token
    }
    payload = {
        'timestamp': timestamp
    }
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response = response.json()
            status = response['status']
            pprint.pprint(response)
            if status == 'found':
                lesson_title = response['new_attempts'][0]['lesson_title']
                lesson_url = response['new_attempts'][0]['lesson_url']
                if response['new_attempts'][0]['is_negative']:
                    status_review = 'Работа не зачтена'
                else:
                    status_review = 'Работа зачтена'
                text = (
                    f"Название урока - {str(lesson_title)}\n"
                    f"Ссылка на урок - {str(lesson_url)}\n"
                    f"Статус проверки - {status_review}"
                )
                send_messange_via_tg_bot(bot, chat_id, updates, text)

            if status == 'timeout':
                timestamp = response['timestamp_to_request']
                if timestamp:
                    try:
                        response = requests.get(url, headers=headers, params=payload)
                        response.raise_for_status()
                        response = response.json()
                        pprint.pprint(response)
                        timestamp = response['timestamp_to_request']
                        continue
                    except:
                        print('Произошла ошибка!')
                        continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            print('Соединение с сетью потеряно')
            time.sleep(5)
            continue


def main():
    load_dotenv()
    chat_id = os.environ.get('TG_CHAT_ID')
    telegram_token = os.environ.get('TG_BOT_TOKEN')
    token_devman = os.environ.get('DEVMAN_TOKEN')
    url_user_reviews = 'https://dvmn.org/api/user_reviews/'
    url_long_polling = 'https://dvmn.org/api/long_polling/'
    bot = telegram.Bot(token=telegram_token)
    updates = bot.get_updates()
    get_review_status(url_long_polling, token_devman, bot, chat_id, updates)


if __name__ == "__main__":
    main()

