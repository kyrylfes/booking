from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import ViewSet

from .models import Hotel, Room, Reservation
from .serializer import HotelSerializer, RoomSerializer, ReservationSerializer


class HotelView(ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk, *args):
        hotel = Hotel.objects.get(id=pk)
        serializer = HotelSerializer(hotel)
        # reservations = []
        #
        # for room in hotel.rooms.all():
        #     room_reserv = room.reservations.all()
        #     for reserv in room_reserv:
        #         reservations.append(
        #             {"id": reserv.id, "start_date": reserv.start_date, "end_date": reserv.end_date,
        #              "user": reserv.user.id})
        # serializer.data['reservations'] = reservations
        # print(serializer.data)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = HotelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.save()

            return JsonResponse({'Status': True}, status=HTTP_200_OK)
        return JsonResponse({'Status': False, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        serializer = HotelSerializer(data=request.data)

        if serializer.is_valid():
            hotel_owner = Hotel.objects.get(id=pk).owner

            if request.user != hotel_owner:
                return JsonResponse({'Status': False, 'Errors': 'You\'re not owner of this hotel/hostel!'},
                                    status=HTTP_400_BAD_REQUEST)
            serializer.update()
            return JsonResponse({'Status': True}, status=HTTP_200_OK)
        return JsonResponse({'Status': False, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        hotel = Hotel.objects.get(id=pk)
        if hotel:
            if request.user != hotel.owner:
                return JsonResponse({'Status': False, 'Errors': 'You\'re not owner of this hotel/hostel!'},
                                    status=HTTP_400_BAD_REQUEST)
            hotel.delete()
            return JsonResponse({'Status': True}, status=HTTP_200_OK)

        return JsonResponse({'Status': False, 'Errors': 'Incorrect ID'}, status=HTTP_400_BAD_REQUEST)


class RoomView(ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            hotel_owner = Hotel.objects.get(id=serializer.validated_data.get('hotel').id).owner
            if request.user != hotel_owner:
                return JsonResponse({'Status': False, 'Errors': 'You\'re not owner of this hotel!'},
                                    status=HTTP_400_BAD_REQUEST)
            serializer.save()
            return JsonResponse({'Status': True}, status=HTTP_200_OK)
        return JsonResponse({'Status': False, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, *args):
        room = Room.objects.get(id=pk)
        serializer = RoomSerializer(room)

        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        request.data['id'] = pk
        serializer = RoomSerializer(data=request.data)

        if serializer.is_valid():
            hotel_owner = Hotel.objects.filter(id=serializer.validated_data.get('hotel')).owner
            if request.user != hotel_owner:
                return JsonResponse({'Status': False, 'Errors': 'You\'re not owner of this room!'},
                                    status=HTTP_400_BAD_REQUEST)
            serializer.update()
            return JsonResponse({'Status': True}, status=HTTP_200_OK)
        return JsonResponse({'Status': False, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        room = Room.objects.get(id=pk)

        if room:
            hotel_owner = Hotel.objects.filter(id=request.data.get('hotel')).owner
            if request.user != hotel_owner:
                return JsonResponse({'Status': False, 'Errors': 'You\'re not owner of this room!'},
                                    status=HTTP_400_BAD_REQUEST)
            room.delete()
            return JsonResponse({'Status': True}, status=HTTP_200_OK)

        return JsonResponse({'Status': False, 'Errors': 'Incorrect ID'}, status=HTTP_400_BAD_REQUEST)


class ReservationView(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')

            if start_date > end_date:
                return JsonResponse({'Status': False, 'Errors': 'Incorrect dates (start date later than end date)'},
                                    status=HTTP_400_BAD_REQUEST)
            serializer.validated_data['user'] = request.user
            serializer.save()

            return JsonResponse({'Status': True}, status=HTTP_200_OK)
        return JsonResponse({'Status': False, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, *args):
        reservation = Reservation.objects.filter(id=pk, user=request.user).first()
        if not reservation:
            return JsonResponse({'Status': False, 'Errors': 'It\'s not your reservation!'},
                                status=HTTP_400_BAD_REQUEST)

        if reservation.user == request.user:
            serializer = ReservationSerializer(reservation)

            return Response(serializer.data)
        return JsonResponse({'Status': False, 'Errors': 'It\'s not your reservation!'}, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')

            if start_date > end_date:
                return JsonResponse({'Status': False, 'Errors': 'Incorrect dates (start date later than end date)'},
                                    status=HTTP_400_BAD_REQUEST)
            reservation = Reservation.objects.filter(id=pk, user=request.user).first()
            if not reservation:
                return JsonResponse({'Status': False, 'Errors': 'It\'s not your reservation!'},
                                    status=HTTP_400_BAD_REQUEST)
            serializer.validated_data['id'] = pk
            serializer.update(reservation, serializer.validated_data)

            return JsonResponse({'Status': True}, status=HTTP_200_OK)
        return JsonResponse({'Status': False, 'Errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        reservation = Reservation.objects.filter(id=pk, user=request.user).first()
        if not reservation:
            return JsonResponse({'Status': False, 'Errors': 'It\'s not your reservation!'},
                                status=HTTP_400_BAD_REQUEST)

        reservation.delete()
        return JsonResponse({'Status': True}, status=HTTP_200_OK)
