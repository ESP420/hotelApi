from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Guest(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.last_name, self.first_name)


class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_por_night = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Price with max
    currency = models.BooleanField( choices=(
    (True, 'BOB'),
    (False, 'USD')
),default=True)   # Currency: US
    capacity = models.IntegerField()  # number of people that can stay in the room
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'-RoomType {self.name} -Description {self.description} -Price por night {self.price_por_night} -capacity {self.capacity}'


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    floor_number = models.IntegerField()
    status = models.BooleanField(choices=(
    (True, 'Free room'),
    (False, 'Occupied room')
),default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'-Type {self.room_type.name} -Room number {self.room_number} -Room floor {self.floor_number} to {self.status}'


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking {self.id} for {self.guest.first_name} from {self.user.first_name}'


class BookingRoom(models.Model):
    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    data_in = models.DateTimeField()
    data_out = models.DateTimeField()
    state = models.IntegerField(choices=[(0, 'Pending'), (1, 'Paid'), (2, 'Removed')], default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'-Booking {self.booking.id} -Room {self.room.room_number} -Flor {self.room.floor_number} from {self.data_in} to  {self.data_out} -state {self.state}'


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.IntegerField(choices=[(0, 'cash'), (1, 'card'), (2, 'qr')], default=0)
    nit = models.IntegerField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'-name {self.name} -nit {self.nit} -amount {self.amount} -Payment method {self.payment_method} -Payment data {self.payment_date}'


class PaymentBookingRoom(models.Model):
    id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    booking_room = models.ForeignKey(BookingRoom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking {self.booking_room.state} -amount {self.payment.amount} from {self.booking_room.data_in} to {self.booking_room.data_out}'
