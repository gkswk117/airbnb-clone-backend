from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound, PermissionDenied
from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistSerializer

# Create your views here.
class SeeAllWishlists(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(all_wishlists, many=True, context={"request":request})
        return Response(serializer.data)
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serializer.errors)

class SeeOneWishlist(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound
    def get(self, request, pk):
        wishlist = self.get_object(pk=pk, user=request.user)
        serializer = WishlistSerializer(wishlist, context={"request":request})
        return Response(serializer.data)
    def put(self, request, pk):
        wishlist = self.get_object(pk=pk, user=request.user)
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            new_wishlist = serializer.save()
            return Response(WishlistSerializer(new_wishlist, context={"request":request}).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        wishlist = self.get_object(pk=pk, user=request.user)
        if request.user != wishlist.user:
            raise PermissionDenied
        wishlist.delete()
        return Response(status=HTTP_200_OK)

class AddRoomToWishlist(APIView):
    permission_classes = [IsAuthenticated]
    def get_wishlist(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound
    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    def put(self, request, pk, room_pk):
        wishlist = self.get_wishlist(pk=pk, user=request.user)
        room =self.get_room(room_pk)
        # print(Wishlist.objects)
        # print(type(Wishlist.objects))
        # print(dir(Wishlist.objects))
        # print(wishlist.room)
        # print(type(wishlist.room))
        # print(dir(wishlist.room))
        if wishlist.rooms.filter(pk=room_pk).exists():
            # wishlit - room은 many to many로 이어져있기 때문에, all(), filter() 메소드를 쓸 수 있다.
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)