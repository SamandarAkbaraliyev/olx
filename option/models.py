from django.db import models

from utils.models import BaseModel


class OptionType(models.TextChoices):
    SELECT = "Select"
    CHOICE = "Choice"
    BUTTON = "Select Button"
    TEXT = "Text"
    NUMBER = "Number"
    MULTIPLE_CHOICE = "Multiple choice"


class Option(BaseModel):
    title = models.CharField(max_length=256)
    type = models.CharField(max_length=32, choices=OptionType.choices)
    code = models.CharField(
        max_length=256, null=True, blank=True
    )
    is_required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class OptionValue(BaseModel):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=256)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.value


class PostOption(BaseModel):
    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="options"
    )
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="posts")
    value = models.CharField(max_length=256, null=True, blank=True)

    @classmethod
    def generate_json_options(cls, post_id):
        data = {"options": []}
        post_options = (
            cls.objects.filter(post_id=post_id)
            .order_by("option__order")
            .select_related(
                "option",
            )
            .prefetch_related("values")
            .prefetch_related(
                "values", "values__option_value"
            )
        )
        for post_option in post_options:
            data["options"].append(
                {
                    "title": post_option.option.title,
                    "value": post_option.value,
                    "values": [
                        values.option_value.value for values in post_option.values.all()
                    ],
                }
            )
            if post_option.option.code == "year":
                data["year"] = post_option.value
            if post_option.option.code == "model":
                for value in post_option.values.all():
                    if value.option_value_extended:
                        if value.option_value_extended.parent:
                            data["model"] = (
                                f"{value.option_value.value} {value.option_value_extended.parent.value}, {value.option_value_extended.value}"
                            )
                        else:
                            data["model"] = (
                                f"{value.option_value.value} {value.option_value_extended.value}"
                            )
                    else:
                        data["model"] = value.option_value.value
        return data

    def __str__(self):
        return f"{self.post} {self.option}"


class PostOptionValue(BaseModel):
    post_option = models.ForeignKey(
        PostOption, on_delete=models.CASCADE, related_name="values"
    )
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post_option", "option_value")


class Plan(BaseModel):
    title = models.CharField(max_length=256)
    plan_detail = models.ManyToManyField('PlanDetail', related_name='plans')

    def __str__(self):
        return self.title


class Plan_Price(BaseModel):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    category = models.ForeignKey('post.Category', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.price


class PlanDetailGroup(BaseModel):
    title = models.CharField(max_length=256)
    is_multiple = models.BooleanField(default=False)
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class PlanDetail(BaseModel):
    group_id = models.ForeignKey(PlanDetailGroup, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=64)
    choice_text = models.CharField(max_length=64, null=True, blank=True)
    amount = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.group_id


class PlanDetailPrice(BaseModel):
    plan_detail = models.ForeignKey(PlanDetail, on_delete=models.CASCADE)
    category = models.ForeignKey('post.Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.price
