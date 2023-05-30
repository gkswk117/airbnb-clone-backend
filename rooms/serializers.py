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
    owner = TinyUserSerializer()
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Room
        fields = "__all__"
        # depth =1
        # depth=1은 아주 아주 간단하고 빠르게 모델의 모든 관계들을 확장시키는 방법
        # 어떤 걸 확장할지 내가 선택해서 커스터마이징하고 싶다면 Meta 앞에 => owner = TinyUserSerializer() 추가.

