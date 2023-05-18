from django.contrib import admin

from api.models import City, Hotel, Room, Reservation

admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Reservation)