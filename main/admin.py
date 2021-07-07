from django.contrib import admin

from .models import Certificate, Account
from django.contrib.auth.models import Group

admin.site.register(Certificate)
admin.site.register(Account)
admin.site.unregister(Group)
