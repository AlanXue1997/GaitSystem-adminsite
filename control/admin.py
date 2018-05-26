from django.contrib import admin
from .models import Person, Door, DoorOpen, Gait, Fingerprint

# Register your models here.

admin.site.register(Person)
admin.site.register(Door)
admin.site.register(DoorOpen)
admin.site.register(Gait)
admin.site.register(Fingerprint)