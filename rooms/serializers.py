from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('name','description')
        
class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['pk', 'name', 'country', 'city', 'price']

class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    # owner에 대한 data는 사용자의 request로 수정되지 않음.
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Room
        fields = "__all__"
        # depth =1
        # depth=1은 아주 아주 간단하고 빠르게 모델의 모든 관계들을 확장시키는 방법
        # 어떤 걸 확장할지 내가 선택해서 커스터마이징하고 싶다면 Meta 앞에 => owner = TinyUserSerializer() 추가.
    """
    def create(self, validated_data):
        print("내가 돌아왔다!")
        print(validated_data)
        return self
    """
    # Serializer.save()를 호출할 때, owner=request.user를 넣어줬다고 해서 create를 정의 해줄 필요 없다. 
    # 아니, create 메소드를 다시 정의해서 Room의 owner에 User의 pk를 넣어줘야되지 않나?
    # No. ModelSerializer가 알아서 해준다.

