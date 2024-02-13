from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('full',views.RoomTypeFull)
urlpatterns = [
    #Guest CRUD
    path('api/List_All_Guest', views.GuestAllViewSet.as_view()), #http://127.0.0.1:8000/api/List_All_Guest
    path('api/Create_Guest', views.GuestCreate.as_view()),#todo #http://127.0.0.1:8000/api/Create_Guest
    path('api/Update_Guest/<id>', views.GuestUpdate.as_view()),#todo #http://127.0.0.1:8000/api/Update_Guest
    path('api/Delete_Guest/<id>', views.GuestDelete.as_view()),#todo #http://127.0.0.1:8000/api/Destroy_Guest
    #Room type CRUD
    path('api/room_type/', include(router.urls)), #http://127.0.0.1:8000/apis/full_room_type/
    #Room CRUD
    path('api/List_All_Room', views.GuestAllViewSet.as_view()), #http://127.0.0.1:8000/api/List_All_Room
    path('api/Create_Room', views.GuestCreate.as_view()),#todo #http://127.0.0.1:8000/api/Create_Room
    path('api/Update_Room/<id>', views.GuestUpdate.as_view()),#todo #http://127.0.0.1:8000/api/Update_Room
    path('api/Delete_Room/<id>', views.GuestDelete.as_view()),#todo #http://127.0.0.1:8000/api/Delete_Room
     #Room CRUD
    path('api/List_All_Room', views.GuestAllViewSet.as_view()), #http://127.0.0.1:8000/api/List_All_Room
    path('api/Create_Room', views.GuestCreate.as_view()),#todo #http://127.0.0.1:8000/api/Create_Room
    path('api/Update_Room/<id>', views.GuestUpdate.as_view()),#todo #http://127.0.0.1:8000/api/Update_Room
    path('api/Delete_Room/<id>', views.GuestDelete.as_view()),#todo #http://127.0.0.1:8000/api/Delete_Room
]
