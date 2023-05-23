from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name= serializers.CharField(required=True, max_length=50)
    kind= serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(read_only=True)
    # 모델과 다르게 정의해도 된다. 어떤 형식으로 보여줄지 내가 정할 수 있다.
    # 예를 들면 pk는 InterField인데, 여기에서는 CharField로 할 수 있다.
    # 근데 뭔가 노가다가 좀 있다. 이건 나중에 다 지우고 django rest framework의 개쩌는 방식으로 바꿀것.

    # Any 'read_only' fields that are incorrectly included in the serializer input will be ignored.
    # 출처: https://www.django-rest-framework.org/api-guide/fields/
    # 따라서 pk와 created_at이 포함된 json을 CategorySerializer에 넣어도 오류는 안나는 것. 그냥 무시하기 때문.