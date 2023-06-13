from rest_framework.serializers import ModelSerializer
from .models import Review
from users.serializers import TinyUserSerializer

class ReviewSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    # GET reviews에 user도 보여지게끔.
    # POST 사용자가 "user":""라고 보낸 걸 받지 않고, 서버에서 user를 입력해 줄 거기 때문에 read_only=True
    class Meta:
        model = Review
        fields = ("user","payload","rating")