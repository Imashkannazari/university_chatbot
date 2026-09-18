from django.contrib import admin

from .models import Category, Field, QAEntry


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order", "name")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order", "name")
    search_fields = ("name",)


@admin.register(QAEntry)
class QAEntryAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "field", "level", "is_active", "order")
    list_filter = ("category", "field", "level", "is_active")
    search_fields = ("question", "answer")
    fields = ("question", "answer", "category", "field", "level", "order", "is_active")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["field"].help_text = "خالی بگذار اگر این سوال برای همه رشته‌ها مشترک است."
        form.base_fields["level"].help_text = "خالی بگذار اگر این سوال برای همه مقاطع مشترک است."
        return form
