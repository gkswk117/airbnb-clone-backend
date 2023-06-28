from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import CreateRoomBookingSerializer, UserBookingSerializer, OwnerBookingSerializer

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
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        all_rooms=Room.objects.all()
        serializer=RoomListSerializer(all_rooms,many=True,context={"request":request})
        return Response(serializer.data)
    def post(self, request):
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        # django는 request 안에 로그인 되어있는 user에 대한 정보를 자동으로 넣어준다.
        # 우리가 따로 설정해두지 않아도 request.user로 갖다 쓰면 된다.
        # 그리고 이 코드는 permission_classes로 대체할 수 있다.
        serializer = RoomDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        category_pk = request.data["category"]
        # 당연 사용자는 request를 보낼 때 pk를 숫자로 직접 입력하지 않는다. 내가 예쁜 UI를 만들어서 선택하게 할 것.
        if not category_pk:
            raise ParseError('Category is required.')
        try:
            category = Category.objects.get(pk=category_pk)
            if not category.kind == Category.CategoryKindChoices.ROOMS:
                raise ParseError("Category's kind is not ROOMS.")
        except Category.DoesNotExist:
            raise ParseError('Cateogry does not exist.')
        # my way
        amenities_pk_list = request.data['amenities']
        amenities_list = []
        for each in amenities_pk_list:
            try:
                amenity = Amenity.objects.get(pk=each)
                amenities_list.append(amenity)
            except Amenity.DoesNotExist:
                raise ParseError(f"Amenity whose id is {each} does not exist.")
        new_room = serializer.save(owner=request.user, category=category, amenities=amenities_list)
        # ManyToMany로 연결된 관계를 저장하는 두 번째 방법. 니코 강의 #11.9의 댓글 참고.
        # 이렇게 하면 애초에 db에 저장을 하기전에 Error를 raise 시키니까 transaction을 쓸 필요도 없음.
        return Response(RoomDetailSerializer(new_room).data)
        
        # Nico's way
    """
    try:
        with transaction.atomic():
        # transaction 안의 모든 코드가 진행될때까지 db상의 어떠한 수정도 이루어지지 않는다.
        # transaction 안의 모든 코드가 진행되면 그제서야 코드 상의 변경점을 한번에 db에 푸시해서 db를 수정한다.
        # 모든 코드가 진행되는 동안 어떠한 에러라도 나면 db를 건드리지 않는다.
        # 밖에서 보기에는 transaction 안에서 db상의 어떠한 에러라도 나면 이전 상태로 원상복구 시키는 것 처럼 보인다.
            new_room = serializer.save(owner=request.user, category=category)
            # Foreign key로 연결된 관계를 저장할 때.
            # save()메서드로 create나 update 메소드의 validated_data에 추가로 데이터를 추가해주고 싶다면,
            # save()메서드를 호출할 때, 데이터를 괄호 안에 추가해주면 끝이다.
            # serializers.py 주석 및 네이버 메모 참고

            print("type of new_room is")
            print(type(new_room))
            # <class 'rooms.models.Room'>

            amenities = request.data['amenities']
            for each in amenities:
                amenity = Amenity.objects.get(pk=each)
                new_room.amenities.add(amenity)
                # ManyToMany로 연결된 관계를 저장하는 첫 번째 방법.
            return Response(RoomDetailSerializer(new_room).data)
    except:
        raise ParseError("Amenity not found")
    """

class SeeOneRoom(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    def get(self, request, pk):
        room=self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request":request})
        print(dir(room))
        print(room.photo_set)
        print(room.city)
        for each in room.photo_set.all():
            print(each.file)
        return Response(serializer.data)
    def put(self, request, pk):
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        # noob
        # category_pk = request.data['category']
        # amenities = request.data['amenities']
        # 이러면 request.data에 category 또는 amenities가 없을 때 에러가 난다.
        
        # pro
        category_pk = request.data.get('category')
        amenities_pk = request.data.get('amenities')
        # 따라서 category 또는 amenities가 없을 때 None을 전달해주기 위해서는 이처럼 get() 메소드를 써줘야 한다.
        # 객체에서 속성값을 가져올때는 직접적으로 가져오지 말고 get() 메소드를 쓰자.
        save_object = {}
        if category_pk:
            try:
                category = Category.objects.get(pk=category_pk)
                if not category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("Category's kind is not ROOMS.")
                save_object["category"] = category
            except Category.DoesNotExist:
                raise ParseError('Cateogry does not exist.')
        if amenities_pk:
            save_object["amenities"]=[]
            for each in amenities_pk:
                try:
                    amenity = Amenity.objects.get(pk=each)
                    save_object["amenities"].append(amenity)
                except Amenity.DoesNotExist:
                    raise ParseError('Amenity whose id is does not exist.')
        print(save_object)
        updated_room = serializer.save(**save_object)
        return Response(RoomDetailSerializer(updated_room, context={"request":request}).data)

    def delete(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
    # transaction 연습용 코드
    def put_v2(self, request, pk):
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_room = serializer.save()
        try:
            category = Category.objects.get(pk=request.data.get("category"))
            if not category.kind == Category.CategoryKindChoices.ROOMS:
                raise ParseError("Category's kind is not ROOMS.")
            updated_room.category = category
        except Category.DoesNotExist:
            raise ParseError('Cateogry does not exist.')
        with transaction.atomic():
            try:
                amenities = request.data.get('amenities')
                #updated_room.amenities.clear()
                for each in amenities:
                    amenity = Amenity.objects.get(pk=each)
                    updated_room.amenities.add(amenity)
                updated_room.save()
                return Response(RoomDetailSerializer(updated_room).data)
            except Amenity.DoesNotExist:
                raise ParseError("Amenity not found")

class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    def get(self, request, pk):
        try:
            page = request.query_params.get('page', 1)
            # url로부터 parameter를 전달받는 방법
            page = int(page)
        except ValueError:
            page = 1
        room = self.get_object(pk)
        print(settings.PAGE_SIZE)
        serializer = ReviewSerializer(room.review_set.all()[settings.PAGE_SIZE*(page-1):settings.PAGE_SIZE*page], many=True)
        # pagination => [n:m] n번째부터 m번째 앞까지 불러오시오.
        # from django.conf import settings => settings.py에 있는 설정값을 불러온다.
        return Response(serializer.data)
    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=room)
            return Response(ReviewSerializer(review).data)
        else:
            return Response(serializer.errors)

class RoomPhotos(APIView):
    permission_classes= [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    def post(self, request, pk):
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        # permission_classes로 대체할 수 있다.
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo= serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)
        
class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        print(now)
        bookings = Booking.objects.filter(room=room, kind=Booking.BookingKindChoices.ROOMS, check_in__gt=now)
        serializer = UserBookingSerializer(bookings, many=True)
        return Response(serializer.data)
    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(user=request.user, kind=Booking.BookingKindChoices.ROOMS, room=room)
            return Response(UserBookingSerializer(booking).data)
        else:
            return Response(serializer.errors)