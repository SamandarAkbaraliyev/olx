from rest_framework import serializers
from post.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'image', 'parent')


class PostSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField(source="json.district")
    photo_count = serializers.IntegerField(source="json.photos_count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "main_photo",
            "district",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField(source="json.district")
    title = serializers.StringRelatedField(source="json.title", read_only=True)
    extended_title = serializers.StringRelatedField(
        source="json.extended_title", read_only=True
    )
    photo_count = serializers.IntegerField(source="json.photos_count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "extended_title",
            "photo_count",
            "main_photo",
            "district",
        )
