from django.db import models
from common.models import CommonModel
"""
# Create your models here.
# expressjs의 mongoose에서 Models의 User.js, Video.js와 같은 작업.
# Session 6 들어가기에 앞서 #5.6에서 기존에 연습용으로 썼던 houses app을 삭제함.
# 그래서 거기에 적혀있던 공부용 메모를 모두 rooms.models.py로 옮겨옴.

# 4.1 Migration
# 모델을 만들고 python manage.py makemigrations으로 migration만들어주기.
# 그리고 python manage.py migrate으로 생성된 migration파일을 데이터베이스에 적용시켜주기
# 모델을 수정할 때도 항상 위와 같은 과정을 거쳐야 한다.

# User model을 customizing하는 방법은 두가지.
# 1) 추가하고 싶은 field를 따로 만들어서(예를 들면 profile을 새로 만들어서) 기존의 장고 user model에 연결짓는 방법.
# 2) 아예 새로 User model을 만드는 방법.
"""
class Room(CommonModel):
    """Room Model Definition"""
    name = models.CharField(max_length=180, default="")
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    descriptioin = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # => 우리가 만든 CommonModel을 상속받았기 때문에 여기에는 안적어줘도 된다.
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")
    kind = models.CharField(max_length=50 ,choices=RoomKindChoices.choices)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    category = models.ForeignKey("categories.Category", on_delete=models.SET_NULL, null=True, blank=True,)
    """
    # 5.5 Foreign Key
    # MongoDB의 populate와 같은 기능. 다른 모델과 연결을 해준다.
    # 다른 모델의 아이디 타입을 ForeignKey라고 한다.
    # First argument => "{application이름}.{model이름}"
    # on_delete => owner에 ID가 저장된 모델이 삭제되었을때 House 모델은 어떻게 할 것인지.

    여기서 만약 owner가 소지하고 있는 room을 보고 싶다면 어떻게 해야할까?
    => 1) noob #7.4 ForeignKey Filter (11:33)
    이 방법의 단점은 한 유저가 가지고 있는 room을 검색하기 위해 모든 room을 전수검사(lookup)해야된다는 점.
    이게 만약 인스타그램이라면? 한 유저가 가지고 있는 사진을 검색하기 위해서 인스타에 있는 모든 사진은 전수검사(lookup)해야됨.
    room.owner.username
    Room.objects.filter(owner__username="gkswk117")
    user.room은 할 수 없을까?
    => 2) pro #7.5 Reverse Accessors (11:27)
    user.room_set.all()
    """
    amenities = models.ManyToManyField("rooms.Amenity")
    # 6.2 Many to Many
    # Foreign Key랑 똑같이 다른 모델과 연결을 해준다. 그 대신 다vs다 연결.
    # First argument => "{application이름}.{model이름}"
    def __str__(self):
       return self.name
    def total_amenities_model(self):
        print(f"total_amenities_model 메소드의 첫번째 인자인 self는 {self}")
        # 위에 정의한 __str__메소드 때문에 인스턴스를 프린트하면 name 속성이 출력된다.
        print(f"type of self is {type(self)}")
        # 인스턴스의 타입을 출력해보면 클래스라고 나온다.
        print(f"self.amenities.all() is {self.amenities.all()}")
        print("\n")
        return "total_amenities_model 입니다. 나는 왜 되냐? + "+str(self.amenities.count())
    def rating_average(self):
        print("im rating")
        if len(self.review_set.all())==0:
            return "리뷰 없음."
        sum =0
        # noob
        # for each in self.review_set.all():
        #     sum = sum+each.rating
        # return round(sum/len(self.review_set.all()),1)
        """
        이렇게 하면 review 안의 필요없는 것들도 다 받아오게 된다.
        효율을 위해 Query 최적화가 필요하다.
        print(self.review_set.all() ㅡㅡ
        vs
        print(self.review_set.all().values("rating")) ^^
        """
        # pro
        for each in self.review_set.all().values("rating"):
            sum = sum+each["rating"]
        return round(sum/len(self.review_set.all().values("rating")),1)   
    
class Amenity(CommonModel):
    """Amenity Definition"""
    name = models.CharField(max_length=150)
    description = models.TextField(default="")
    def __str__(self):
       return self.name
    #2.5 에서 배웠던 내용. 클래스를 print할 때 내가 원하는 것으로 출력하고 싶으면 __str__메서드의 리턴값에 집어넣기.
    # underscroe method에 대한 자세한 내용은 네이버 메모 참고
    """
    class Meta:
        verbose_name_plural = "Amenities"
    """

    """
    Many To One => models.ForeignKey 이용
    [Room1, Room2, Room3] => User1
    Room은 하나의 User만 가질 수 있고, User는 여러 Room을 가질 수 있다.
    """
    
    """
    One To One => models.OneToOneField 이용
    Experience1 => Video1
    Experience는 하나의 Video만 가질 수 있고, Video는 하나의 Experience만 가질 수 있다.
    """
    
    """
    Many To Many => models.ManyToManyField 이용
    [Amenity1, Amenity2, Amenity3] => [Room1, Room2, Room3]
    Amenity는 여러 Room을 가질 수 있고, Room은 여러 Amenity를 가질 수 있다.
    """



