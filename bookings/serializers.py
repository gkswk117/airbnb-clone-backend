from django.utils import timezone
from rest_framework import serializers
from .models import Booking

class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
     
    class Meta:
        model = Booking
        fields = ("check_in", "check_out", "guests")
    # view.py가 아닌 serializer.py에서 데이터 추가 검증하기.
    # user가 보낸 date가 미래 날짜가 아닐 때 is_valid() 메서드가 false를 반환하도록 하면 어떨까?
    def validate_check_in(self, value):
        # value는 data= 을 통해 serializer 안으로 들어온 데이터 중 check_in field에 해당하는 값.
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!!!!")
        # 이로서 is_valid() 메서드는 false를 반환한다.
        return value
    def validate_check_out(self, value):
        print("value는")
        print(value)
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        # 이로서 is_valid() 메서드는 false를 반환한다.
        return value
    def validate(self, data):
        print(data)
        # data는 data= 을 통해 serializer 안으로 들어온 데이터 dict.
        if data.get("check_in") > data.get("check_out"):
            raise serializers.ValidationError("Check-out date should be later than Check-in date.")
        if Booking.objects.filter(
            check_in__lte=data.get("check_out"),
            check_out_gte=data.get("check_in"),
        ).exists():
            raise serializers.ValidationError("Another Booking is already exists on that period.")
        return data
class UserBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "guests")

class OwnerBookingSerializer(serializers.ModelSerializer):
    pass