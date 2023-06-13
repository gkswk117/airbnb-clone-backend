from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('name','description')
        
class RoomListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    def get_rating(self, room):
        return room.rating_average()
    is_owner = SerializerMethodField()
    def get_is_owner(self, room):
        return self.context.get("request").user == room.owner
    class Meta:
        model = Room
        fields = ['pk', 'name', 'country', 'city', 'price','rating','is_owner']

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
        # get_rating을 호출할 때 SerializerMethodField는 알아서 (???)를 넣어준다.
        return room.rating_average()
    is_owner = SerializerMethodField()
    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return request.user == room.owner
        else:
            return "확인할 수 없습니다."       

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