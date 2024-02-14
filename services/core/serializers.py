from rest_framework import serializers
from .models import Guest
from .models import Room
from .models import RoomType
from .models import Booking
from .models import BookingRoom
from .models import Payment
from .models import PaymentBookingRoom


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'last_name', 'first_name', 'phone', 'identity_card_number']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'description', 'price_por_night', 'currency', 'capacity']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_type', 'room_number', 'floor_number', 'status']


class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRoom
        fields = ['id', 'booking', 'room', 'data_in', 'data_out', 'state']


class BookingSerializer(serializers.ModelSerializer):
    booking_rooms = BookingRoomSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'guest', 'user', 'booking_rooms']

    def create(self, validated_data):
        booking_rooms_data = validated_data.pop('booking_rooms', [])
        booking = Booking.objects.create(**validated_data)
        for booking_room_data in booking_rooms_data:
            BookingRoom.objects.create(booking=booking, **booking_room_data)
        return booking


class PaymentBookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentBookingRoom
        fields = ['id', 'payment', 'booking_room', 'is_deleted']


class PaymentSerializer(serializers.ModelSerializer):
    payment_booking_rooms = PaymentBookingRoomSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'payment_method', 'nit', 'name', 'is_deleted',
                  'payment_booking_rooms']

    def create(self, validated_data):
        payment_booking_rooms_data = validated_data.pop('payment_booking_rooms', [])
        payment = Payment.objects.create(**validated_data)
        for payment_booking_room_data in payment_booking_rooms_data:
            BookingRoom.objects.create(payment=payment, **payment_booking_room_data)
        return payment
