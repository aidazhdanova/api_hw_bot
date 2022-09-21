class SendMessageException(Exception):
    """Исключение отправки сообщения."""

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
