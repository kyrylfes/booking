from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Hotel, Room, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'room', 'start_date', 'end_date', 'user')
        read_only_fields = ('id', 'user')
        extra_kwargs = {'start_date': {'required': True},
                        'end_date': {'required': True},
                        'email': {'required': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True},
                        'email': {'required': True}}


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'hotel', 'bathroom_count', 'bed_count', 'toilet_count', 'description', 'size', 'kitchen',
                  'freewifi', 'tv', 'dishwasher', 'air_conditioning', 'price')
        read_only_fields = ('id',)


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'owner', 'rate', 'city', 'rooms')
        read_only_fields = ('id',)
