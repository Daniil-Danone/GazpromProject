from django.db import models


class GazpromUser(models.Model):
    login = models.EmailField(unique=True, primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    isAdmin = models.BooleanField(default=False)  # False = stuff; True = Admin
    isDeveloper = models.BooleanField(default=False)
    isLogin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{str(self.login)} | {self.name} {self.surname} | Админ: {self.isAdmin} -- Разработчик: {self.isDeveloper}'


class Well(models.Model):
    id = models.AutoField(primary_key=True)
    conditions = models.CharField(max_length=255, null=True)
    geo = models.CharField(max_length=255, null=True)
    status = models.IntegerField()  # 1 - рабочая; 2 - законсервированная; 3 - требуется ремонт
    created_at = models.DateTimeField(auto_now_add=True)
    last_check = models.DateTimeField(null=True)

    def __str__(self):
        return f'Скважина: {str(self.id)} | • Статус {self.status}'


class Check(models.Model):
    id = models.AutoField(primary_key=True)
    well_id = models.ForeignKey('Well', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'Проверка: {str(self.id)} | {str(self.well_id)}'
