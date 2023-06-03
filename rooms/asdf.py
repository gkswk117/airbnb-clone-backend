    def put_v2(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_room = serializer.save()
        try:
            category = Category.objects.get(pk=request.data.get("category"))
            if not category.kind == Category.CategoryKindChoices.ROOMS:
                raise ParseError("Category's kind is not ROOMS.")
            updated_room.category = category
        except Category.DoesNotExist:
            raise ParseError('Cateogry does not exist.')
        with transaction.atomic():
            try:
                amenities = request.data.get('amenities')
                #updated_room.amenities.clear()
                for each in amenities:
                    amenity = Amenity.objects.get(pk=each)
                    updated_room.amenities.add(amenity)
                updated_room.save()
                return Response(RoomDetailSerializer(updated_room).data)
            except Amenity.DoesNotExist:
                raise ParseError("Amenity not found")
            





    def put(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        # updated_room = serializer.save()
        
        # noob
        # category_pk = request.data['category']
        # amenities = request.data['amenities']
        # 이러면 request.data에 category 또는 amenities가 없을 때 에러가 난다.
        
        # pro
        category_pk = request.data.get('category')
        amenities_pk = request.data.get('amenities')
        # category 또는 amenities가 없을 때 None을 전달해주기 위해서는 이처럼 get() 메소드를 써줘야 한다.
        # 객체에서 속성값을 가져올때는 직접적으로 가져오지 말고 get() 메소드를 쓰자.
        save_object = {}
        if category_pk:
            try:
                category = Category.objects.get(pk=category_pk)
                if not category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("Category's kind is not ROOMS.")
                save_object["category"] = category
            except Category.DoesNotExist:
                raise ParseError('Cateogry does not exist.')
        if amenities_pk:
            save_object["amenities"]=[]
            for each in amenities_pk:
                try:
                    amenity = Amenity.objects.get(pk=each)
                    save_object["amenities"].append(amenity)
                except Amenity.DoesNotExist:
                    raise ParseError('Amenity whose id is does not exist.')
        print(save_object)
        updated_room = serializer.save(**save_object)
        return Response(RoomDetailSerializer(updated_room).data)
