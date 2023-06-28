from rest_framework.test import APITestCase
from . import models
# Create your tests here.
class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESCRIPTION = "Amenity Test"
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESCRIPTION)
        
    def test_all_amenities(self):
        # self.client는 API로 get/post/put/delete request를 보낼 수 있다.
        response = self.client.get("/api/v1/rooms/amenities/")
        print("response는")
        print(response)
        data = response.json()
        print(data)
        # 실제 데이터베이스는 건드리지 않고 테스팅을 해야되기 때문에 새로운 빈 데이버베이스를 만든다.
        # 그리고 테스팅이 끝나면 소멸된다.
        # 따라서 지금은 빈 배열을 받을 것.
        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].get("name"), self.NAME)
        self.assertEqual(data[0].get("description"), self.DESCRIPTION)
    def test_create_amenity(self):
        NEW_AMENITY_NAME = "New Amenity"
        NEW_AMENITY_DESCRIPTION = "New Amenity desc."
        response = self.client.post("/api/v1/rooms/amenities/", data={"name":NEW_AMENITY_NAME, "description":NEW_AMENITY_DESCRIPTION})
        data = response.json()
        self.assertEqual(response.status_code, 200, "Not 200 status code")
        self.assertEqual(data["name"], NEW_AMENITY_NAME)
        self.assertEqual(data["description"], NEW_AMENITY_DESCRIPTION)
        response = self.client.post("/api/v1/rooms/amenities/")
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)
