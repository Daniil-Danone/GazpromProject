from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Сначала вызовите обработчик исключений по умолчанию для REST framework,
    # чтобы получить стандартный ответ об ошибке.
    response = exception_handler(exc, context)

    # Теперь добавьте в ответ код состояния HTTP.
    if response is not None:
        try:
            if response.data['login']:
                response.data = "ERROR: пользователь c данным логином уже существует"
            elif response.data['password']:
                response.data = "ERROR: неправильный пароль"
            elif response.data['detail']:
                response.data = "ERROR: у вас нет прав на использование данного функционала"
        except:
            pass

        # response.data['status_code'] = response.status_code

    return response
