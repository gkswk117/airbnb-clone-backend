from rest_framework.serializers import ModelSerializer
from .models import Photo, Video
from rooms.serializers import RoomDetailSerializer

class PhotoSerializer(ModelSerializer):
    room = RoomDetailSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ('pk', 'file', 'description', 'room')