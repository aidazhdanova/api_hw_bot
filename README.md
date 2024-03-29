Телеграм-бот, уведомляющий о статусе выполненной домашней работы.

## Функциональность бота

- Каждые 10 минут бот обращается к API сервиса Практикум.Домашка, проверяя текущий статус отправленной на ревью домашней работы.
- При изменении статуса бот анализирует ответ от API и отправляет соответствующее уведомление через Телеграм.
- Весь процесс работы бота логируется, и в случае возникновения важных проблем бот отправляет сообщение об ошибке в Телеграм.

## Развертывание проекта локально
1. Клонируем репозиторий в нужную директорию:
- git clone https://github.com/aidazhdanova/api_hw_bot.git

2. Создаём виртуальное окружение:
- Для Mac:
  ```
  python3 -m venv venv
  ```

4. Активируем виртуальное окружение:
- Для Mac:
  ```
  source venv/bin/activate
  ```

4. Устанавливаем зависимости:
- pip install -r requirements.txt

5. Создаём файл `.env` и указываем в нём необходимые переменные окружения:
- `PRACTICUM_TOKEN` (ссылка: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a)
- `TELEGRAM_TOKEN` (@BotFather)
- `TELEGRAM_CHAT_ID` (@userinfobot)

6. Запускаем программу в терминале:
python3 homework.py


