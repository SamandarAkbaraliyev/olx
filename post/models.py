import random
import string

from django.utils.text import slugify
from django.db import models

from utils.models import BaseModel


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Region(BaseModel):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class District(BaseModel):
    title = models.CharField(max_length=256)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="districts"
    )

    def __str__(self):
        return self.title


class Category(BaseModel):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(null=True, blank=True)
    has_price = models.BooleanField(default=True)
    has_free = models.BooleanField(default=True)
    has_exchange = models.BooleanField(default=True)
    options = models.ManyToManyField(
        "option.Option",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Subcategory(BaseModel):
    title = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title


class Post(BaseModel):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=64)

    published_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=128, null=True, blank=True)
    views = models.IntegerField(default=0)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='posts')

    json = models.JSONField(null=True, blank=True)

    contact_name = models.CharField(max_length=64)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + '-' + rand_slug(), allow_unicode=True)
        super().save(*args, **kwargs)


class Photo(BaseModel):
    image = models.ImageField(upload_to="photos")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="photos")
    is_main = models.BooleanField(default=False)

    @classmethod
    def get_main_photo(cls, post_id):
        photo = Photo.objects.filter(post_id=post_id, is_main=True).first()
        print(photo)
        if photo:
            return photo.image
        return None
