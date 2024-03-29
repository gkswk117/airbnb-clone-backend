from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("pk", "name", "description")


class RoomListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    photo_set = PhotoSerializer(read_only=True, many=True)

    def get_rating(self, room):
        return room.rating_average()

    is_owner = SerializerMethodField()

    def get_is_owner(self, room):
        return self.context.get("request").user == room.owner

    is_wishlist = SerializerMethodField()

    def get_is_wishlist(self, room):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return None
        return Wishlist.objects.filter(user=request.user, rooms__id=room.pk).exists()

    class Meta:
        model = Room
        fields = [
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "is_wishlist",
            "photo_set",
        ]


class RoomDetailSerializer(ModelSerializer):
    # Model에서 ForeignKey가 저장되어있는 field는 그냥 ForeignKey(id, 숫자)만 보여진다.
    # depth=1은 모든 걸 다 보여준다.
    # Representing foreign key values in Django serializers => Using a nested serializer
    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    # Reverse Accessor라고 해서 다를게 없다. 위의 owner, category, amenities랑 똑같다.
    photo_set = PhotoSerializer(read_only=True, many=True)
    # review_set = ReviewSerializer(read_only=True, many=True)
    # 하지만 review의 경우 이 방법은 모든 review를 다 가지고 오기 때문에, 너무 많은 데이터를 가져오게된다.
    # review가 10,000개면 10,000개를 한번에 다 불러올거? ㄴㄴ
    # 그래서 사용할 것이 pagination

    """
    # name, city, country, address field는 request.data를 그대로 validated_data에 넣을 것.
    # owner, category, amenities field는 request.data로는 숫자(pk)만 전달받고, 서버 메소드에서 해당 pk를 가진 인스턴스를 검색해서 따로 넣어줄 것.
    # new_room = serializer.save(owner=request.user, category=category, amenities=amenities_list)
    """

    # Custom Field
    # 원래는 Model에 있는 field만 ModelSerializer에서 field로 쓸 수 있지만,
    # SerializerMethodField를 통해 custom field를 만들 수 있다.
    rating = SerializerMethodField()

    def get_rating(self, room):
        # get_rating을 호출할 때 SerializerMethodField는 알아서 object를 넣어준다.
        # 여기서 object는 views.py에서 serialize 된 room object를 뜻한다.
        # => serializer = RoomDetailSerializer(room, context={"request":request})
        return room.rating_average()

    is_owner = SerializerMethodField()

    def get_is_owner(self, room):
        request = self.context.get("request")
        if not request:
            return "요청(requset)이 없습니다."
        if not request.user:
            return "유저(user)가 없습니다."
        else:
            return request.user == room.owner

    is_wishlist = SerializerMethodField()

    def get_is_wishlist(self, room):
        request = self.context.get("request")
        if not request:
            return "요청(requset)이 없습니다."
        if not request.user:
            return "유저(user)가 없습니다."
        if request.user.is_authenticated:
            return Wishlist.objects.filter(
                user=request.user, rooms__id=room.pk
            ).exists()
        return False
        # user=request.user이고 id=room.pk인 room을 가지고 있는 wishlist를 가져온다.
        # To span a relationship in Django Lookups, use the field name of related fields across models,
        # separated by double underscores, until you get to the field you want.
        # https://docs.djangoproject.com/en/4.2/topics/db/queries/#lookups-that-span-relationships

    class Meta:
        model = Room
        fields = "__all__"
        # depth =1
        # depth=1은 아주 아주 간단하고 빠르게 모델의 모든 관계들을 확장시키는 방법
        # 어떤 걸 확장할지 내가 선택해서 커스터마이징하고 싶다면 Meta 앞에 => owner = TinyUserSerializer() 추가.

    # def create(self, validated_data):
    #     print("ModelSerializer에서도 save()를 실행했을때 create() or update() 메소드가 실행되는지 확인용!!!")
    #     print(validated_data)
    #     return

    # Serializer.save()를 호출할 때, owner=request.user를 넣어줬다고 해서 create를 정의 해줄 필요 없다.
    # 아니, create 메소드를 다시 정의해서 Room의 owner에 User의 pk를 넣어줘야되지 않나?
    # No.
    # save()메서드로 create나 update 메소드의 validated_data에 추가로 데이터를 추가해주고 싶다면,
    # save()메서드를 호출할 때, 데이터를 괄호 안에 owner면 user 객체 전체를, category면 category 객체 전체를 추가해주면 끝이다.
    # 나머지는 ModelSerializer가 알아서 해준다.
