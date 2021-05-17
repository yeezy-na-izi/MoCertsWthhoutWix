from django.contrib import admin

from .models import MyCertsUser, Certificate

admin.site.register(MyCertsUser)
admin.site.register(Certificate)