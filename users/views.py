from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def register(request):
    data = request.data
    User.objects.create_user(
        username=data['email'],
        email=data['email'],
        password=data['password']
    )
    return Response({"message": "User registered"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "email": request.user.email,
        "first_name": request.user.first_name
    })
