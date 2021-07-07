from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, photo='', password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            photo=photo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    email = models.EmailField(verbose_name='email', max_length=120)
    username = models.CharField(verbose_name='username', max_length=60)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name='first name', max_length=30)
    last_name = models.CharField(verbose_name='last name', max_length=60)
    # phone = models.CharField(verbose_name='phone', max_length=15, blank=True, default=0)
    photo = models.ImageField(verbose_name='photo', blank=True, default='', upload_to='account/static/profile')
    # about_me = models.TextField(verbose_name='about me', blank=True, default='')
    # mail_notify = models.BooleanField(verbose_name='mail', default=True)
    # telegram_notify = models.BooleanField(verbose_name='telegram', default=False)
    # vk = models.BooleanField(verbose_name='vk', default=False)
    certificate = models.ForeignKey('Certificate', on_delete=models.SET_NULL, null=True, blank=True)
    telegram_id = models.BigIntegerField(verbose_name='telegram id', blank=True, default=0)
    balance = models.IntegerField(verbose_name='balance', default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    objects = MyAccountManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active


class Certificate(models.Model):
    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    STATUS = [
        ('NONE', ''),
        ('RECEIVED', 'Получен'),
        ('PAID', 'Оплачен'),
    ]
    number = models.BigIntegerField(verbose_name='Номер сертификата')
    url = models.URLField(max_length=255, verbose_name='Ссылка на сертификат')
    nominal = models.IntegerField(verbose_name='Номинал', default=1)
    user1 = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='first_users')
    user2 = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='second_users')
    user3 = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='third_users')
    published_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    certificate_image = models.ImageField(default=None)
    made_by = models.ForeignKey(Account, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                related_name='made_by_user')
    status = models.CharField(max_length=15, choices=STATUS, default='NONE')

    def get_absolute_url(self):
        return f"https://mocerts.com/certificate/{self.number}"
