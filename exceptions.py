class NoSendMessage(Exception):
    """Исключение для случаев, когда не нужно отправлять сообщение в Telegram."""

    pass


class APIException(Exception):
    """Исключение проблем с запросом к API."""

    pass


class CheckResponseException(Exception):
    """Исключение некорректного формата ответа API."""

    pass


class HWStatusException(Exception):
    """Исключение неизвестного статуса домашки."""

    pass
