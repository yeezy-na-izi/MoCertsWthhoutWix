from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.urls import reverse


class MyCertsUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    tlg_id = models.IntegerField(name='telegram_id', null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name='phone', null=True, blank=True)
    balance = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='balance', blank=False, default=0)
    certificate = models.ForeignKey('Certificate', on_delete=models.SET_NULL, null=True, blank=True)
    profile_photo = models.ImageField(default='profile.png')

    def __str__(self):
        return f'Пользователь {self.user.username}'


class Certificate(models.Model):
    STATUS = [
        ('NONE', ''),
        ('RECEIVED', 'Получен'),
        ('PAID', 'Оплачен'),
    ]
    number = models.BigIntegerField(verbose_name='Номер сертификата')
    url = models.URLField(max_length=255, verbose_name='Ссылка на сертификат')
    nominal = models.IntegerField(verbose_name='Номинал', default=1)
    user1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='first_users')
    user2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='second_users')
    user3 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='third_users')
    published_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    certificate_image = models.ImageField(default=None)
    made_by = models.ForeignKey(MyCertsUser, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                related_name='made_by_user')
    status = models.CharField(max_length=15, choices=STATUS, default='NONE')

    def get_absolute_url(self):
        return "https://mocerts.com/certificate/{}".format(self.number)
