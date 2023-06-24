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
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        # 이로서 is_valid() 메서드는 false를 반환한다.
        return value
    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        # 이로서 is_valid() 메서드는 false를 반환한다.
        return value

class UserBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "guests")

class OwnerBookingSerializer(serializers.ModelSerializer):
    pass