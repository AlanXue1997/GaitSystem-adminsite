from django.contrib import admin
from .models import Person, Door, DoorOpen

# Register your models here.

admin.site.register(Person)
admin.site.register(Door)
admin.site.register(DoorOpen)