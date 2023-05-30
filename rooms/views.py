from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
# Create your views here.
# (2) rest api for react

class SeeAllAmenities(APIView):
    def get(self,request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity= serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors)

class SeeOneAmenity(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
    def get(self,request,pk):
        serializer = AmenitySerializer(self.get_object(pk))
        return Response(serializer.data)
    def put(self,request,pk):
        serializer = AmenitySerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class Rooms(APIView):
    def get(self, request):
        all_rooms=Room.objects.all()
        serializer=RoomListSerializer(all_rooms,many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_room = serializer.save()
            return Response(RoomDetailSerializer(new_room).data)
        else:
            return Response(serializer.errors)

class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    def get(self, request, pk):
        serializer = RoomDetailSerializer(self.get_object(pk))
        return Response(serializer.data)
    def put(self, request, pk):
        serializer = RoomDetailSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            updated_room = serializer.save()
            Response(RoomDetailSerializer(updated_room).data)
        else:
            Response(serializer.errors)
    def delete(self, request, pk):
        pass
