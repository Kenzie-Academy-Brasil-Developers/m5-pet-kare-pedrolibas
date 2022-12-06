from rest_framework.views import APIView, Response, Request, status
from .models import Pet
from .serializers import PetSerializer
from django.shortcuts import get_object_or_404


class PetView(APIView):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        print("teste patch")
        serializer = PetSerializer(pet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

