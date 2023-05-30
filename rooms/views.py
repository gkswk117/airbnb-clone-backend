from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from .models import Amenity, Room
from categories.models import Category
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

class SeeAllRooms(APIView):
    def get(self, request):
        print(request.user)
        all_rooms=Room.objects.all()
        serializer=RoomListSerializer(all_rooms,many=True)
        return Response(serializer.data)
    def post(self, request):
        if request.user.is_authenticated:
            # django는 request안에 로그인 되어있는 user에 대한 정보를 자동으로 넣어준다.
            # 우리가 따로 설정해두지 않아도 request.user로 갖다 쓰면 된다.
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data["category"]
                # 당연 사용자는 request를 보낼 때 pk를 직접 입력하지 않는다. 내가 예쁜 UI를 만들어서 선택하게 할 것.
                if not category_pk:
                    raise ParseError('Category is required.')
                else:
                    try:
                        category = Category.objects.get(pk=category_pk)
                        if not category.kind == Category.CategoryKindChoices.ROOMS:
                            raise ParseError("Category's kind is not ROOMS.")
                    except Category.DoesNotExist:
                        raise ParseError('Cateogry does not exist.')
                    new_room = serializer.save(owner=request.user, category=category)
                    # Foreign key로 연결된 관계를 저장할 때.
                    # save()메서드로 create나 update 메소드의 validated_data에 추가로 데이터를 추가해주고 `싶다면,
                    # save()메서드를 호출할 때, 데이터를 괄호 안에 추가해주면 끝이다.
                    # serializers.py 주석 및 네이버 메모 참고

                    print("type of new_room is")
                    print(type(new_room))
                    # <class 'rooms.models.Room'>

                    amenities = request.data['amenities']
                    for each in amenities:
                        try:
                            amenity = Amenity.objects.get(pk=each)
                        except Amenity.DoesNotExist:
                            raise ParseError(f'Amenity whose id is {each} does not exist.')
                            #or pass
                        new_room.amenities.add(amenity)
                        # ManyToMany로 연결된 관계를 저장할 때.
                        # 이 때는 단순히 new_room.amenities = amenity로 할 수 없다.
                    return Response(RoomDetailSerializer(new_room).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated

class SeeOneRoom(APIView):
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
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
