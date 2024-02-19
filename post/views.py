from rest_framework import generics
from post import models
from post import serializers


class CategoryParentListAPIView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(parent=None)
        return qs


class CategoryListAPIView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        parent = self.kwargs.get('parent')
        category = models.Category.objects.get(slug=parent)
        qs = qs.filter(parent__id=category.id)
        return qs


class MainPostListAPIView(generics.ListAPIView):
    queryset = models.Post.objects.all().order_by('?')[:12]
    serializer_class = serializers.PostSerializer
    filterset_fields = ('category', 'price')


class PostListAPIView(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    filterset_fields = ('category', 'price')


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostDetailSerializer
    lookup_field = 'slug'

