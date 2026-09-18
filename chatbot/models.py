from django.db import models


class Field(models.Model):

    name = models.CharField("نام رشته", max_length=150, unique=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "رشته تحصیلی"
        verbose_name_plural = "رشته‌های تحصیلی"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField("نام دسته", max_length=100, unique=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class QAEntry(models.Model):

    LEVEL_CHOICES = [
        ("kardani", "کاردانی"),
        ("karshenasi", "کارشناسی"),
        ("arshad", "کارشناسی ارشد"),
        ("phd", "دکتری"),
    ]

    question = models.TextField("سوال")
    answer = models.TextField("جواب")

    category = models.ForeignKey(
        Category,
        verbose_name="دسته‌بندی",
        related_name="entries",
        on_delete=models.CASCADE,
    )

    field = models.ForeignKey(
        Field,
        verbose_name="رشته تحصیلی (خالی = برای همه رشته‌ها)",
        related_name="entries",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    level = models.CharField(
        "مقطع تحصیلی (خالی = برای همه مقاطع)",
        max_length=20,
        choices=LEVEL_CHOICES,
        blank=True,
    )

    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    class Meta:
        verbose_name = "سوال و جواب"
        verbose_name_plural = "سوال و جواب‌ها"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.question[:60]
