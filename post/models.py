import random
import string

from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from utils.models import BaseModel
from option.models import PostOption


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


class Status(models.TextChoices):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    IN_PROCESS = 'In process'
    NOT_PAID = 'Not paid'


class Price_type(models.TextChoices):
    PRICE = 'Price'
    FREE = 'Free'
    EXCHANGE = 'Exchange'


class Category(BaseModel):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='category/photos/', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    options = models.ManyToManyField(
        "option.Option", blank=True, null=True
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
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Post(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=64)

    price = models.IntegerField(null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=128, null=True, blank=True)
    views_count = models.IntegerField(default=0)
    main_photo = models.ImageField(upload_to='photos', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='posts')

    json = models.JSONField(null=True, blank=True)

    contact_name = models.CharField(max_length=64)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', null=True)
    status = models.CharField(max_length=64, choices=Status.choices, default=Status.INACTIVE)
    price = models.IntegerField(null=True, blank=True)
    price_type = models.CharField(max_length=64, choices=Price_type.choices, default=Price_type.PRICE)

    def make_json_fields(self):
        data = {
            "title": "",
            "extended_title": "",
            "year": "",
            "model": "",
            "district": "",
            "photos_count": 0,
            "options": [],
        }
        data.update(**PostOption.generate_json_options(self.id))
        data["district"] = self.district.title
        data["photos_count"] = self.photos.count()
        data["title"] = f"{data['model']}"
        data["extended_title"] = f"{data['model']} {data['year']} {self.price}  y.e."
        return data

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + '-' + rand_slug(), allow_unicode=True)
        super().save(*args, **kwargs)


class Photo(BaseModel):
    image = models.ImageField(upload_to="photos")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="photos")
    is_main = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    @classmethod
    def get_main_photo(cls, post_id):
        photo = Photo.objects.filter(post_id=post_id, is_main=True).first()
        if photo:
            return photo.image
        return None



