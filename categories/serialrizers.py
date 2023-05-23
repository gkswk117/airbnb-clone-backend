from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    name= serializers.CharField(required=True)
    kind= serializers.CharField()
    created_at = serializers.DateTimeField()
    # 모델과 다르게 정의해도 된다. 어떤 형식으로 보여줄지 내가 정할 수 있다.
    # 예를 들면 pk는 InterField인데, 여기에서는 CharField로 할 수 있다.
    # 근데 뭔가 노가다가 좀 있다. 이건 나중에 다 지우고 django rest framework의 개쩌는 방식으로 바꿀것.