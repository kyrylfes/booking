from django.urls import path, include
from rest_framework import routers
from django.contrib.auth import views as auth_views

from .views import HotelView, RoomView, ReservationView

router = routers.SimpleRouter()
router.register(r'hotels', HotelView, basename='hotels')
router.register(r'rooms', RoomView, basename='rooms')
router.register(r'reservations', ReservationView, basename='reservations')

urlpatterns = [
  path('', include(router.urls)),
  path('auth/', include('djoser.urls')),
  path('auth/', include('djoser.urls.authtoken')),
  path('auth/', include('djoser.urls.jwt'))
]
