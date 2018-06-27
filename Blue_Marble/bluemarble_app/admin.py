from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import UserInfo,RoomInfo,Board


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(RoomInfo)
admin.site.register(Board)