from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Hotel(models.Model):
    TYPE = [
        ('hostel', 'Hostel'),
        ('hotel', 'Hotel')
    ]

    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(choices=TYPE, default='hotel')
    owner = models.ForeignKey(User, related_name='hotels', on_delete=models.SET_NULL, null=True,
                              blank=True)
    rate = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    city = models.ForeignKey('City', related_name='hotels', on_delete=models.CASCADE)

    # rooms

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='rooms', on_delete=models.CASCADE)
    bathroom_count = models.PositiveIntegerField()
    bed_count = models.PositiveIntegerField()
    toilet_count = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    size = models.PositiveIntegerField()
    kitchen = models.BooleanField(default=0)
    freewifi = models.BooleanField(default=0)
    tv = models.BooleanField(default=0)
    dishwasher = models.BooleanField(default=0)
    air_conditioning = models.BooleanField(default=0)
    price = models.PositiveIntegerField()

    # reservations

    def __str__(self):
        return f'{self.hotel} Room №{self.id}'


class Reservation(models.Model):
    room = models.ForeignKey('Room', related_name='reservations', on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room}:{self.start_date}--{self.end_date}'


class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    # hotels

    def __str__(self):
        return self.name
