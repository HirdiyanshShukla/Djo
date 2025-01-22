from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message

admin.site.register(Room)
# THIS TELLS DJANGO THAT WE WANT TO CONTROL THIS TABLE FROM THE ADMIN PANNEL
admin.site.register(Topic)
admin.site.register(Message) 
