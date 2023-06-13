from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Photo, Video
#from rooms.serializers import RoomDetailSerializer

class PhotoSerializer(ModelSerializer):
    # room = RoomDetailSerializer(read_only=True)
    # Representing 할때만 nested serializer가 필요하고, Updating or Creating 할때는 RoomSerializer가 필요없다.
    # 여기서 RoomDetailSerializer를 가져오면 양 싸이드로 가져온거라서 에러가 뜬다.
    room_name = SerializerMethodField()
    def get_room_name(self, photo):
        print(self)
        print(photo)
        return photo.room.name
    class Meta:
        model = Photo
        fields = ('pk', 'file', 'description', 'room_name')