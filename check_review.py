import requests
import time
import os
import telegram
from dotenv import load_dotenv
from message_sender import send_message_via_tg_bot


def get_review_status(token_devman, telegram_token, chat_id):
    url = 'https://dvmn.org/api/long_polling/'
    text = ''
    timestamp = None
    headers = {
        'Authorization': f'Token {token_devman}'
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
                send_message_via_tg_bot(telegram_token, chat_id, text)

            if status == 'timeout':
                timestamp = response['timestamp_to_request']
                if timestamp:
                    try:
                        response = requests.get(url, headers=headers, params=payload)
                        response.raise_for_status()
                        response = response.json()
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
    chat_id = os.environ['TG_CHAT_ID']
    telegram_token = os.environ['TG_BOT_TOKEN']
    token_devman = os.environ['DEVMAN_TOKEN']
    get_review_status(token_devman, telegram_token, chat_id)


if __name__ == "__main__":
    main()

