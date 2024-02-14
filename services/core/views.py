from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import generics, viewsets, status, mixins
from rest_framework.response import Response
from .models import Booking, BookingRoom, Guest, Payment, PaymentBookingRoom, Room, RoomType
from .serializers import BookingRoomSerializer, BookingSerializer, GuestSerializer, PaymentBookingRoomSerializer, \
    PaymentSerializer, RoomTypeSerializer, RoomSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json


# Create your views here.


# Curd of Guest
class GuestAllViewSet(generics.ListAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = (AllowAny,)


class GuestCreate(generics.CreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = (IsAuthenticated,)


class GuestUpdate(generics.UpdateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class GuestDelete(generics.DestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Guest deleted successfully"
        },
            status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class RoomTypeFull(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Room type deleted successfully"
        },
            status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


# room
class RoomFull(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Room deleted successfully"
        },
            status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


# booking guest room record

class CombinedBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        created_booking_rooms = []
        booking_serializer = BookingSerializer(data=request.data)
        if booking_serializer.is_valid():
            booking = booking_serializer.save()
            booking_rooms_data = request.data.get('booking_rooms', [])
            for booking_room_data in booking_rooms_data:
                booking_room_data['booking'] = booking.id
                booking_room_serializer = BookingRoomSerializer(data=booking_room_data)
                if booking_room_serializer.is_valid():
                    booking_room = booking_room_serializer.save()
                    created_booking_rooms.append(booking_room)
                    # Perform any additional logic here, such as associating the booking_room with the booking
                else:
                    return Response({'booking_rooms': booking_room_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            booking_rooms_data = BookingRoomSerializer(created_booking_rooms, many=True).data
            return Response({'booking': booking_serializer.data, 'booking-rooms': booking_rooms_data,
                             'message': 'Booking and booking rooms created successfully.'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# booking rooms
class BookingRoomAllViewSet(generics.ListAPIView):
    queryset = BookingRoom.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = (AllowAny,)


class BookingRoomCreate(generics.CreateAPIView):
    queryset = BookingRoom.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = (IsAuthenticated,)


class BookingRoomUpdate(generics.UpdateAPIView):
    queryset = BookingRoom.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class BookingRoomDelete(generics.DestroyAPIView):
    queryset = BookingRoom.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Booking room type deleted successfully"
        },
            status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        payment_serializer = PaymentSerializer(data=request.data)
        if payment_serializer.is_valid():
            payment = payment_serializer.save()
            payment_booking_rooms_data = request.data.get('payment_booking_rooms', [])
            for payment_booking_room_data in payment_booking_rooms_data:
                payment_booking_room_serializer = PaymentBookingRoomSerializer(data=payment_booking_room_data)
                if payment_booking_room_serializer.is_valid():
                    payment_booking_room_serializer.save(payment=payment)
                else:
                    return Response({'payment_booking_rooms': payment_booking_room_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'payment': payment_serializer.data, 'message': 'Payment and related records created successfully.'},
                status=status.HTTP_201_CREATED)
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        payment_serializer = PaymentSerializer(instance, data=request.data, partial=partial)
        if payment_serializer.is_valid():
            payment = payment_serializer.save()
            payment_booking_rooms_data = request.data.get('payment_booking_rooms', [])
            for payment_booking_room_data in payment_booking_rooms_data:
                payment_booking_room_id = payment_booking_room_data.get('id')
                if payment_booking_room_id:
                    payment_booking_room = PaymentBookingRoom.objects.get(id=payment_booking_room_id)
                    payment_booking_room_serializer = PaymentBookingRoomSerializer(payment_booking_room,
                                                                                   data=payment_booking_room_data,
                                                                                   partial=partial)
                else:
                    payment_booking_room_serializer = PaymentBookingRoomSerializer(data=payment_booking_room_data,
                                                                                   partial=partial)
                if payment_booking_room_serializer.is_valid():
                    payment_booking_room_serializer.save()
                else:
                    return Response({'payment_booking_rooms': payment_booking_room_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'payment': payment_serializer.data, 'message': 'Payment and related records updated successfully.'},
                status=status.HTTP_200_OK)
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CombinedPaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        created_payment_rooms = []
        payment_serializer = PaymentSerializer(data=request.data)
        if payment_serializer.is_valid():
            payment = payment_serializer.save()
            payment_booking_rooms_data = request.data.get('payment_booking_rooms', [])
            for payment_booking_room in payment_booking_rooms_data:
                payment_booking_room['payment'] = payment.id
                payment_room_serializer = PaymentBookingRoomSerializer(data=payment_booking_room)
                if payment_room_serializer.is_valid():
                    payment_room = payment_room_serializer.save()
                    created_payment_rooms.append(payment_room)
                    # Perform any additional logic here, such as associating the payment_room with the payment
                else:
                    return Response({'payment_rooms': payment_room_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            payment_rooms_data = PaymentBookingRoomSerializer(created_payment_rooms, many=True).data
            return Response({'payment': payment_serializer.data, 'payment-booking-rooms': payment_rooms_data,
                             'message': 'Payment is successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        payment_serializer = PaymentSerializer(instance, data=request.data, partial=partial)
        if payment_serializer.is_valid():
            payment = payment_serializer.save()
            payment_booking_rooms_data = request.data.get('payment_booking_rooms', [])
            for payment_booking_room_data in payment_booking_rooms_data:
                payment_booking_room_id = payment_booking_room_data.get('id')
                if payment_booking_room_id:
                    payment_booking_room = PaymentBookingRoom.objects.get(id=payment_booking_room_id)
                    payment_booking_room_serializer = PaymentBookingRoomSerializer(payment_booking_room,
                                                                                   data=payment_booking_room_data,
                                                                                   partial=partial)
                else:
                    payment_booking_room_serializer = PaymentBookingRoomSerializer(data=payment_booking_room_data,
                                                                                   partial=partial)
                if payment_booking_room_serializer.is_valid():
                    payment_booking_room_serializer.save()
                else:
                    return Response({'payment_booking_rooms': payment_booking_room_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'payment': payment_serializer.data, 'message': 'Payment and related records updated successfully.'},
                status=status.HTTP_200_OK)
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# new user
class UserCreate(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        if User.objects.filter(username=username).exists():
            return Response({'username': ['A user with this username already exists.']})

        if User.objects.filter(email=email).exists():
            return Response({'email': ['A user with this email already exists.']})

        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = request.data['first_name']
        new_user.last_name = request.data['last_name']
        new_user.is_staff = request.data['staff']
        new_user.save()
        user_key = Token.objects.create(user=new_user)
        data = {'detail': 'User created successfully', 'token': user_key.key}
        return Response(data, content_type="application/json", status=status.HTTP_201_CREATED)
