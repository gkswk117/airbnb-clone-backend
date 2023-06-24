from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Booking

class UserBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "guests")

class OwnerBookingSerializer(ModelSerializer):
    pass