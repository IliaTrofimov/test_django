from django.contrib import admin

from .models import Message, BannedUser


admin.site.register(Message)
admin.site.register(BannedUser)