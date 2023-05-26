from rest_framework import serializers
from .models import Category
class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name= serializers.CharField(required=True, max_length=50)
    kind= serializers.ChoiceField(choices=Category.CategoryKindChoices.choices)
    created_at = serializers.DateTimeField(read_only=True)
    # 모델과 다르게 정의해도 된다. 어떤 형식으로 보여줄지 내가 정할 수 있다.
    # 예를 들면 pk는 InterField인데, 여기에서는 CharField로 할 수 있다.
    # 근데 뭔가 노가다가 좀 있다. 이건 나중에 다 지우고 django rest framework의 개쩌는 방식으로 바꿀것.

    # Any 'read_only' fields that are incorrectly included in the serializer input will be ignored.
    # 출처: https://www.django-rest-framework.org/api-guide/fields/
    # 따라서 pk와 created_at이 포함된 json을 CategorySerializer에 넣어도 오류는 안나는 것. 그냥 무시하기 때문.

    # serializers.Serializer의 메소드 및 속성
    # errors
    # save()

    def create(self, validated_data):
        # serializer.save()를 호출하면 인스턴스의 내부에 create 또는 update라고 정의되어있는 함수를 호출한다.
        # serializers.Serializer => BaseSerializer 코드 참고.
        return Category.objects.create(**validated_data)
        return Category.objects.create(
            name=validated_data['name'],
            kind=validated_data['kind']
        )
        # **: python 문법 
        # dictionary 에서 각 속성을 풀어서 변수에 할당할 때 쓴다.
        # my_dict = {'a': 1, 'b': 2, 'c': 3}
        # my_function(**my_dict)
        # my_function(a=1, b=2, c=3)
        # 위 두개는 같은 표현이다.
        # 주의점 => 매개변수로 전달되는 dictionary의 속성명(key)과 함수 안에서 쓰는 변수명이 같아야 한다.
        # my_fuction안에서도 똑같이 a,b,c로 써야 된다.
        # test3.py 참고, chatGPT history 참고