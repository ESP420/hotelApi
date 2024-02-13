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
        fields = ['id', 'last_name', 'first_name', 'phone']

        
class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id','name', 'description', 'price_por_night', 'capacity']

        