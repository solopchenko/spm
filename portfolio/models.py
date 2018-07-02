from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ServiceStatus(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "сатус услуги"
        verbose_name_plural = "статусы услуг"


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Описание')
    notes = models.TextField(blank=True, verbose_name='Заметки', help_text='Заметки недоступны заказчику')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    customer = models.CharField(max_length=200, verbose_name='Заказчик', blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Стоимость (руб.)', default=0, blank=True)
    costs = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Затраты (руб.)', default=0, blank=True)
    importance = models.IntegerField(verbose_name='Важность', default=1, blank=True)
    value = models.IntegerField(verbose_name='Ценность', default=1, blank=True)
    status = models.ForeignKey(
        ServiceStatus,
        on_delete=models.SET_NULL,
        verbose_name='Статус',
        null=True
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Валаделец',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

def get_full_name(self):
    full_name = self.get_full_name()
    if full_name:
        return full_name
    return self.username

class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Описание')
    trello = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    deadline_at = models.DateTimeField(verbose_name='Плановая дата завершения', blank=True, null=True)
    assign_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Назначенный пользователь',
        related_name='assign_user',
        blank=True,
        null=True
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Создатель',
        related_name='creator',
        blank=True,
        null=True
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        verbose_name='Услуга',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"

class Notification(models.Model):
    name = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    notify_at = models.DateTimeField(verbose_name='Время уведомления')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Назначенный пользователь',
        blank=True,
        null=True
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        verbose_name='Услуга',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"

User.add_to_class("__str__", get_full_name)
User.add_to_class("__unicode__", get_full_name)
