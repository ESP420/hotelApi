from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Full_Room_Type', views.RoomTypeFull)
router.register('Full_Room', views.RoomFull)
router.register('Full_Booking', views.CombinedBookingViewSet)
router.register('Full_Payments', views.CombinedPaymentViewSet, basename='payment')

urlpatterns = [
    # Guest CRUD
    path('api/List_All_Guest', views.GuestAllViewSet.as_view()),  # http://127.0.0.1:8000/api/List_All_Guest
    path('api/Create_Guest', views.GuestCreate.as_view()),  # todo #http://127.0.0.1:8000/api/Create_Guest
    path('api/Update_Guest/<id>', views.GuestUpdate.as_view()),  # todo #http://127.0.0.1:8000/api/Update_Guest
    path('api/Delete_Guest/<id>', views.GuestDelete.as_view()),  # todo #http://127.0.0.1:8000/api/Destroy_Guest
    # Room type CRUD # http://127.0.0.1:8000/apis/Full_Room_Type/
    # Room CRUD # http://127.0.0.1:8000/apis/Full_Room/
    # booking guest and booking room combined create record # http://127.0.0.1:8000/apis/full_booking/
    path('apis/', include(router.urls)),
    # Guest CRUD
    path('api/List_All_Booking_Room', views.BookingRoomAllViewSet.as_view()),
    # http://127.0.0.1:8000/api/List_All_Booking_Room
    path('api/Create_Booking_Room', views.BookingRoomCreate.as_view()),
    # todo #http://127.0.0.1:8000/api/Create_Booking_Room
    path('api/Update_Booking_Room/<id>', views.BookingRoomUpdate.as_view()),
    # todo #http://127.0.0.1:8000/api/Update_Booking_Room
    path('api/Delete_Booking_Room/<id>', views.BookingRoomDelete.as_view()),
    # todo #http://127.0.0.1:8000/api/Destroy_Booking_Room
    path('api/Create_User', views.UserCreate.as_view())
]
