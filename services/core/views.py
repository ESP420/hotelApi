from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Guest, RoomType
from .serializers import GuestSerializer, RoomTypeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.


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
            "message":"Guest deleted successfully"
        },
        status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
#Room type
    
class RoomTypeFull(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = (IsAuthenticated,)