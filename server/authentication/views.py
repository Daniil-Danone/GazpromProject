import re
import requests
from rest_framework import (generics, views)
from rest_framework.response import Response
from .models import GazpromUser, Well, Check
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import GazpromUserSerializer, WellSerializer, CheckSerializer, GazpromUserListSerializer


# # Получение токена авторизации
# def get_auth_token(login, password):
#
#     # Запрос на добавление пользователя в django-auth
#     data1 = {"email": login, "username": login, "password": password}
#     requests.post('http://127.0.0.1:8000/api/v1/auth/users/', data=data1).json()
#
#     # Запрос на получение данных из django-auth
#     data2 = {"username": login, "password": password}
#
#     # Возврат токена
#     return requests.post('http://127.0.0.1:8000/auth/token/login/', data=data2).json()["auth_token"]


def update_wells_last_check(well_id, datetime):
    well = Well.objects.get(id=well_id)
    well.last_check = datetime
    well.save()


# Представление всех пользователей (при наличии токена)
class UsersAPIList(views.APIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({'users': GazpromUserListSerializer(GazpromUser.objects.all(), many=True).data})


# Представление входа на сайт (для всех)
class UserAPILogin(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response("Метод GET не поддерживается")

    def post(self, request):

        # Проверка на правильность ввода логина
        if 'login' in request.data.keys():
            login = request.data['login']
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if re.match(pattern, login):
                if 'password' in request.data.keys():
                    password = request.data['password']
                    try:
                        # сверяем, есть ли в БД пользователь с данным логином
                        user = GazpromUser.objects.get(login=login)

                        # сверяем введённый пароль с тем, что хранится в БД
                        if password == user.password:

                            # Присваиваем токен сессии пользователю, а также отмечаем, что пользователь залогинен
                            user = GazpromUser.objects.get(login=login)
                            # user.token = get_auth_token(login, password)
                            user.isLogin = True
                            user.save()

                            # Возвращаем JSON-объект c данными о пользователе в фронтенд
                            return Response(GazpromUserSerializer(user).data)

                        # Кастомная обработка всех возможных ошибок
                        else:
                            return Response('ERROR: Неправильный пароль')
                    except BaseException:
                        return Response(f"ERROR: Пользователь {login} не существует")
                else:
                    return Response("ERROR: Введите пароль")
            else:
                return Response("ERROR: Неверный формат почты")
        else:
            return Response("ERROR: Введите почту")


# Представление регистрации на сайт (для всех)
class UserAPIRegistration(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response("Метод GET не поддерживается")

    def post(self, request):

        # Проверка на правильность ввода логина
        if 'login' in request.data.keys():
            login = request.data["login"]
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if re.match(pattern, login) is not None:
                if 'password' in request.data.keys():
                    password = request.data["password"]

                    # Проверка на правильность ввода логина
                    if len(password) >= 8:
                        # Смотрим, есть ли в БД пользователь с данным логином
                        try:
                            if GazpromUser.objects.get(login=login):
                                return Response(f"ERROR: Пользователь {login} уже существует")

                        except:
                            # Прогоняем данные через сериализатор
                            serializer = GazpromUserSerializer(data=request.data)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                            # Присваиваем новый токен сессии пользователю
                            # user = GazpromUser.objects.get(login=login)
                            # user.token = get_auth_token(login, password)
                            # user.save()

                            # Возвращаем JSON-объект c данными о пользователе в фронтенд
                            return Response(serializer.data)

                        # Кастомная обработка всех возможных ошибок
                    else:
                        return Response("ERROR: Минимальная длина пароля - 8 символов")
                else:
                    return Response("ERROR: Введите пароль")
            else:
                return Response("ERROR: Неверный формат почты")
        else:
            return Response("ERROR: Введите почту")


class UserAPIDelete(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    queryset = GazpromUser.objects.all()
    serializer_class = GazpromUserSerializer


class WellAppend(views.APIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({'users': WellSerializer(Well.objects.all(), many=True).data})

    def post(self, request):
        serializer = WellSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        update_wells_last_check(serializer.data['id'], serializer.data['created_at'])

        # Возвращаем JSON-объект c данными о пользователе в фронтенд
        return Response(serializer.data)


class WellAPIView(views.APIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({"wells": WellSerializer(Well.objects.all(), many=True).data})


class CheckAppend(views.APIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({'users': CheckSerializer(Check.objects.all(), many=True).data})

    def post(self, request):
        serializer = CheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        update_wells_last_check(serializer.data['id'], serializer.data['created_at'])

        # Возвращаем JSON-объект c данными о пользователе в фронтенд
        return Response(serializer.data)


class ChecksAPIView(views.APIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({"checks": CheckSerializer(Check.objects.all(), many=True).data})
