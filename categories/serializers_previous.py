from rest_framework import serializers
from .models import Category
class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name= serializers.CharField(required=True, max_length=50)
    kind= serializers.ChoiceField(choices=Category.CategoryKindChoices.choices)
    created_at = serializers.DateTimeField(read_only=True)
    # 모델과 다르게 정의해도 된다. 어떤 형식으로 받을지 내가 정할 수 있다.
    # 예를 들면 pk는 InterField인데, 여기에서는 CharField로 할 수 있다.
    # 다만, 모델과 형식이 똑같아야지 POST 요청으로 받은 데이터를 그대로 데이터베이스에 넣을 수 있겠지.
    # 근데 뭔가 노가다가 좀 있다. 이건 나중에 다 지우고 django rest framework의 개쩌는 방식(ModelSerializer)으로 바꿀것.

    # Any 'read_only' fields that are incorrectly included in the serializer input will be ignored.
    # 출처: https://www.django-rest-framework.org/api-guide/fields/
    # 따라서 pk와 created_at이 포함된 json을 CategorySerializer에 넣어도 오류는 안나는 것. 그냥 무시하기 때문.

    # Section 10에서 배우는 serializers.Serializer의 속성 및 메소드
    # errors
    # save()

    def create(self, validated_data):
        # serializer.save()를 호출하면 인스턴스의 내부에 create 또는 update라고 정의되어있는 함수를 호출한다.
        # serializers.Serializer => BaseSerializer 코드 참고.
        print(validated_data)
        # validated_data에는 views.py에서 Serializer를 호출할 때 data={}에 담긴 데이터가 들어있다.
        created_instance = Category.objects.create(**validated_data)
        # (chatGPT)Model.objects.create()) returns a newly created instance of the model class.
        # It represents the object that was just created and saved to the database.
        return created_instance
    # **: python 문법 
    # dictionary의 각 속성을 풀어서 변수에 할당할 때 쓴다.
    """
    validated_data
    == {"name": "Vehicle", "kind": "experiences"} 이므로,
    Category.objects.create(**validated_data)
    <=> Category.objects.create(name="Vehicle", kind="experiences") 와 똑같다.
    
    ex)
    my_dict = {'a': 1, 'b': 2, 'c': 3}
    my_function(**my_dict)
    my_function(a=1, b=2, c=3)
    위 두개는 같은 표현이다.
    주의점 => 매개변수로 전달되는 dictionary의 속성명(key)과 함수 안에서 쓰는 변수명이 같아야 한다.
    my_fuction안에서도 똑같이 a,b,c로 써야 된다.
    test3.py 참고, chatGPT history 참고
    """

    def update(self, instance, validated_data):
        # QuerySet과 Class 인스턴스가 서로 헷갈려서 작성한 연습용 코드
        # print(type(Category.objects.filter(pk=1)))#QuerySet (필터링 조건을 만족하는 Category 인스턴스들의 배열)
        # <class 'django.db.models.query.QuerySet'>
        # print(type(Category.objects.get(pk=1)))#Class 인스턴스 (get 조건을 만족하는 하나의 Category 인스턴스)
        # <class 'categories.models.Category'>

        # nico's way.
        # Using the save() method of a model instance.
        """
        # dict 메소드 get() 이용
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        """
        # hanwoong's way.
        # Using the update() method of a queryset.
        updated_count = instance.update(**validated_data)
        # (chatGPT)Model.objects.update() returns an integer representing the number of records that were updated in the database.
        # queryset 중 총 몇 개의 instance가 update되었는지 그 개수를 return한다.
        # (chatGPT)The update() method can only be called on a queryset, not on a single object.
        # Therefore, calling update() directly after get() will raise an AttributeError because the update() method is not available on a single object.
        return updated_count