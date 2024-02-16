from django.contrib import admin
from post.models import Category, Subcategory, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'id')
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'id')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Post)


