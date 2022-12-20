from rest_framework import (filters,
                            mixins,
                            viewsets)
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .permissions import PermissionReviewComment, IsAdminOrSuperUserOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework import serializers

from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
                             UserSerializer,
                             ReviewSerializer,
                             CommentSerializer)

from reviews.models import Category, Genre, Title, Review, Comment


def send_confirmation_code(request):
    serializer = UserSerializer(data=request.data)
    pass


def token_access(request):
    pass


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pass

    def me(self):
        pass


class ListAddDeleteViewSet(mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListAddDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrSuperUserOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class GenreViewSet(ListAddDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrSuperUserOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [PermissionReviewComment]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        queryset = Review.objects.filter(
            title=title_id,
            author=self.request.user)
        if len(queryset) > 0:
            raise serializers.ValidationError(
                'Нельзя два раза писать отзыв на одно произведение!'
            )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [PermissionReviewComment]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
