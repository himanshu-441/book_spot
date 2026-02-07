from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, recommend_books

router = DefaultRouter()
router.register('books', BookViewSet)

urlpatterns = [
    path('recommend/', recommend_books),
]

urlpatterns += router.urls

