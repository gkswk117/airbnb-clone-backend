from rest_framework import serializers
from .models import Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        # or fields = ("name","kind")
        # or exclude = ("pk", "created_at", "uploaded_at")
    # ㄴㅇㄱ 끝? 개.쩐.다. 단 네 줄. 이게 모두 ModelSerializer 덕분.
    # 심지어 create, update 메소드도 자동으로 구현되어 있다.