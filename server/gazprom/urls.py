from django.contrib import admin
from django.urls import path, include, re_path

from authentication.views import UserAPIRegistration, UserAPILogin, UsersAPIList, UserAPIDelete, \
    WellAppend, WellAPIView, CheckAppend, ChecksAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth', include("rest_framework.urls")),
    path('api/v1/get-users', UsersAPIList.as_view()),
    path('api/v1/login', UserAPILogin.as_view()),
    path('api/v1/registration', UserAPIRegistration.as_view()),
    # path('api/v1/logout', UserAPILogout.as_view()),
    path('api/v1/deleteuser/<str:pk>', UserAPIDelete.as_view()),
    path('api/v1/get-wells', WellAPIView.as_view()),
    path('api/v1/create-well', WellAppend.as_view()),
    path('api/v1/get-checks', ChecksAPIView.as_view()),
    path('api/v1/create-check', CheckAppend.as_view()),
    path('api/v1/auth/', include("djoser.urls")),
    re_path(r'^auth/', include("djoser.urls.authtoken"))
]
