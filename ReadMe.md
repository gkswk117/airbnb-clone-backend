### Rooms

GET POST /rooms
GET PUT DELETE /rooms/1
GET /rooms/1/amenities
GET POST /rooms/1/reviews
GET POST /amenities
GET PUT DELETE /amenities/1
POST /rooms/1/photos
DELETE /rooms/1/photos/1

### Wishlists

GET POST /wishlists
GET PUT DELETE /wishlists/1
PUT /wishlists/1/rooms/2
is_liked

### Users

GET PUT /mypage
POST /users
GET /users/username
POST /users/log-in
POST /users/log-out
POST /users/change-password

아래였다가 #12.0에서 갑자기 위로 바뀜.

POST /users
GET /users/rooms
GET /users/rooms
GET /users/experiences
GET /users/bookings
GET PUT /users/1
GET /users/1/reviews

# Experiences [코드 챌린지]

GET POST /experiences
GET PUT DELETE /experiences
GET /experiences/1/perks
GET POST /perks
GET PUT DELETE /perks/1
GET POST /experiences/1/bookings
GET PUT DELETE /experiences1/bookings/2
GET POST /rooms/1/bookings
GET PUT DELETE /rooms/1/bookings/2

# request 관련 로그 확인 차 Django 내부 코드 수정한거 "#삭제하기"로 메모 남겨둠.