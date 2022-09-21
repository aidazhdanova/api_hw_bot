import os
import time
import logging

import requests
import telegram
from http import HTTPStatus
from dotenv import load_dotenv

import exceptions


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)


def send_message(bot, message):
    """Функция отправки сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Успех! Бот отправил сообщение: {message}')
    except Exception as error:
        raise SystemError(f'Не отправляются сообщения: {error}')


def get_api_answer(current_timestamp):
    """Функция выполняет запрос к API Яндекс Практикума."""
    logger.info('Запрос к серверу')
    timestamp = current_timestamp or int(time.time())
    if not isinstance(timestamp, (float, int)):
        raise TypeError('Ошибка формата даты')
    params = {
        'from_date': timestamp
    }
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
    except requests.exceptions.RequestException as error:
        raise exceptions.APIException(f'Не удается найти Endpoint: {error}')

    if response.status_code != HTTPStatus.OK:
        message = (f'Endpoint {ENDPOINT} не работает, '
                   f'http status: {response.status_code}')
        raise exceptions.APIException(message)

    try:
        response = response.json()
    except Exception as error:
        raise Exception(f'Ошибка получения json: {error}')
    return response


def check_response(response):
    """Функция проверяет корректность ответа API Яндекс Практикума."""
    logger.info('Проверка API ответа на корректность')
    try:
        homeworks_list = response['homeworks']
    except KeyError as key:
        message = f'Ошибка доступа по ключу homeworks: {key}'
        logger.error(message)
        raise exceptions.CheckResponseException(message)

    if homeworks_list is None:
        message = 'В API ответе нет словаря с домашними работами'
        logger.error(message)
        raise exceptions.CheckResponseException(message)

    if not isinstance(homeworks_list, list):
        message = 'В API ответе домашние работы представлены не списком'
        logger.error(message)
        raise exceptions.CheckResponseException(message)
    if 'current_date' not in response.keys():
        message_current_date = 'Ключ "current_date" отсутствует в словаре'
        raise KeyError(message_current_date)
    return homeworks_list


def parse_status(homework):
    """Функция возвращает сообщение о изменении статуса проверки."""
    logger.info('Проверка статуса проверки')
    if 'homework_name' not in homework:
        parse_status = 'Ошибка доступа по ключу homework_name'
        logger.error(parse_status)
        raise KeyError(parse_status)

    if 'status' not in homework:
        parse_status = 'Ошибка доступа по ключу status'
        logger.error(parse_status)
        raise KeyError(parse_status)

    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')

    try:
        verdict = VERDICTS[homework_status]
    except KeyError:
        message = 'Неизвестный статус домашней работы'
        logger.error(message)
        raise exceptions.HWStatusException(message)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Функция проверки наличия токена и чат id телеграмма."""
    logger.info('Проверка токена и id')
    tokens = {
        'telegram_chat_id': TELEGRAM_CHAT_ID,
        'practicum_token': PRACTICUM_TOKEN,
        'telegram_token': TELEGRAM_TOKEN
    }
    for key, value in tokens.items():
        if value is None:
            logging.critical(f'{key} отсутствует')
            return False
    return True


def main():
    """Основная логика работы бота."""
    logger.info('Запуск бота')
    if not check_tokens():
        exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    error = ''

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            current_timestamp = response.get('current_date')

            if len(homeworks) > 0:
                send_message(bot, parse_status(homeworks[0]))
            else:
                logger.info('Не нашлось новых статусов')

        except Exception as err:
            message = f'Сбой в работе программы: {err}'
            logger.critical(message)
            if message != error:
                send_message(bot, message)

        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
