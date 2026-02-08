from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .recommender import recommend
from .utils import find_best_book_match



class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_books(request):
    user_input = request.data.get('user_input')

    if not user_input:
        return Response(
            {"error": "user_input is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ STEP 1: Find best DB match
    best_match = find_best_book_match(user_input)

    if not best_match:
        return Response(
            {
                "message": "No close match found in database",
                "recommendations": []
            },
            status=status.HTTP_200_OK
        )

    # ✅ STEP 2: Pass canonical name to recommender
    recommended_data = recommend(best_match)

    return Response(
        {
            "matched_book": best_match,
            "recommendations": recommended_data
        },
        status=status.HTTP_200_OK
    )


