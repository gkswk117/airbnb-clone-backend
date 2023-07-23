from rest_framework.test import APITestCase
from . import models
from users.models import User
# Create your tests here.
class TestAmenities(APITestCase):
    NAME = "Amenities Test"
    DESCRIPTION = "Amenities Test"
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESCRIPTION)
    def message_status_code(self, status_code):
        return f"TestAmenities Failed. Response.status_code should be {status_code} status code"
    def test_see_all_amenities(self):
        # self.client는 APITestCase의 메소드로 우리의 TestAmenities 클래스가 상속 받은 것.
        # self.client는 API로 get/post/put/delete request를 보낼 수 있다.
        # 모든 amenities를 받아오는 request 테스트
        response = self.client.get("/api/v1/rooms/amenities/")
        print("response는")
        print(response)
        data = response.json()
        print(data)
        # 실제 데이터베이스는 건드리지 않고 테스팅을 해야되기 때문에 새로운 빈 데이버베이스를 만든다.
        # 그리고 테스팅이 끝나면 소멸된다.
        # 따라서 지금은 print(data)를 했을 때 빈 배열이 출력된다.
        self.assertEqual(response.status_code, 200, self.message_status_code(200))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].get("name"), self.NAME)
        self.assertEqual(data[0].get("description"), self.DESCRIPTION)
    def test_create_amenity(self):
        NEW_AMENITY_NAME = "New Amenity"
        NEW_AMENITY_DESCRIPTION = "New Amenity desc."
        # 데이터베이스에 amenity 추가할 때(정상 작동)
        response = self.client.post("/api/v1/rooms/amenities/", data={"name":NEW_AMENITY_NAME, "description":NEW_AMENITY_DESCRIPTION})
        data = response.json()
        self.assertEqual(response.status_code, 200, self.message_status_code(200))
        self.assertEqual(data["name"], NEW_AMENITY_NAME)
        self.assertEqual(data["description"], NEW_AMENITY_DESCRIPTION)
        # 데이터 없이 request를 보냈을 때 테스트(400 오류)
        response = self.client.post("/api/v1/rooms/amenities/")
        data = response.json()
        self.assertEqual(response.status_code, 400, self.message_status_code(400))
        self.assertIn("name", data)

class TestAmenity(APITestCase):
    NAME = "Amenity Test"
    DESCRIPTION = "Amenity Test"
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESCRIPTION)
    def message_status_code(self, status_code):
        return f"TestAmenity Failed. Response.status_code should be {status_code} status code"
    def test_see_one_amenity(self):
        # 데이터 베이스에 없는 amenity를 가져올 때(404 오류)
        response =self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(response.status_code, 404, self.message_status_code(404))
        # 데이터 베이스에 있는 amenity를 가져올 때(정상 작동)
        response =self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200, self.message_status_code(200))
        data=response.json()
        self.assertEqual(data["name"],self.NAME)
        self.assertEqual(data["description"],self.DESCRIPTION)

    def test_put_amenity(self):
        """
        code challenge
        """
        pass
    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        print("slsislsy")
        self.assertEqual(response.status_code, 204, self.message_status_code(204))

class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user= user
    def message_status_code(self, status_code):
        return f"TestRooms Failed. Response.status_code should be {status_code} status code"
    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        print(response)
        self.assertEqual(response.status_code, 403, self.message_status_code(403))
        
        self.client.login(username="test",password="123")
        # self.client.force_login(self.user)
        response = self.client.post("/api/v1/rooms/")
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 400, self.message_status_code(400))