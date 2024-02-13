from django.contrib import admin
from .models import Guest
from .models import Room
from .models import RoomType
from .models import Booking
from .models import BookingRoom
from .models import Payment
from .models import PaymentBookingRoom

# Register your models here.
admin.site.register(Guest)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(BookingRoom)
admin.site.register(Payment)
admin.site.register(PaymentBookingRoom)
