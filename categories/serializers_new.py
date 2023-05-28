from rest_framework.serializers import ModelSerializer
from .models import Category

# (중요!)이 serializer를 사용하고 싶으면 serializer의 첫번째인자로 반드시 a single object를 전달하시오.
# Model.objects.filter()대신 Model.objects.get()을 사용하시오.

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        # or fields = ("name","kind")
        # or exclude = ("pk", "created_at", "uploaded_at")
    # ㄴㅇㄱ 끝? 개.쩐.다. 단 네 줄. 이게 모두 ModelSerializer 덕분.
    # 심지어 create, update 메소드도 자동으로 구현되어 있다.