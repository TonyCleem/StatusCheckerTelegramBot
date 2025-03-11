import telegram
import os
from dotenv import load_dotenv


def send_messange_via_tg_bot(telegram_token, chat_id, text):
    bot = telegram.Bot(token=telegram_token)
    updates = bot.get_updates()
    first_name = updates[0]['message']['chat']['first_name']
    bot.send_message(chat_id=chat_id, text=f'{first_name}, преподаватель проверил работу')
    bot.send_message(chat_id=chat_id, text=text)


def main():
    load_dotenv()
    text = ''
    chat_id = os.environ['TG_CHAT_ID']
    telegram_token = os.environ['TG_BOT_TOKEN']
    send_messange_via_tg_bot(telegram_token, chat_id, text)


if __name__ == '__main__':
    main()