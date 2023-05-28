from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Amenity
from .serializers import AmenitySerializer
# Create your views here.
# (2) rest api for react

class SeeAllAmenities(APIView):
    def get(self,request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity= serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors)

class SeeOneAmenity(APIView):
    def get(self,request,pk):
        pass
    def put(self,request,pk):
        pass
    def delete(self,request,pk):
        pass