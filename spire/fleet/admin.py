from django.contrib import admin
from .models import Blimp, Service, Invite
# Register your models here.

admin.site.register([Blimp, Service, Invite])
