
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Category, Field, QAEntry

VALID_LEVELS = {code for code, _label in QAEntry.LEVEL_CHOICES}


def _parse_filters(request):
    
    field_id = request.GET.get("field")
    level = request.GET.get("level") or None

    if field_id:
        if not field_id.isdigit() or not Field.objects.filter(pk=field_id).exists():
            return None, None, JsonResponse({"error": "رشته معتبر نیست."}, status=400)
        field_id = int(field_id)
    else:
        field_id = None

    if level and level not in VALID_LEVELS:
        return None, None, JsonResponse({"error": "مقطع معتبر نیست."}, status=400)

    return field_id, level, None


def _matching_entries(field_id, level):
    """QAEntry های فعالی که با رشته/مقطع انتخابی کاربر سازگارند (یا عمومی‌اند)."""
    queryset = QAEntry.objects.filter(is_active=True)

    if field_id is not None:
        queryset = queryset.filter(Q(field_id=field_id) | Q(field__isnull=True))
    else:
        queryset = queryset.filter(field__isnull=True)

    if level:
        queryset = queryset.filter(Q(level=level) | Q(level=""))
    else:
        queryset = queryset.filter(level="")

    return queryset


@require_GET
def fields_view(request):
    fields = Field.objects.all().values("id", "name")
    return JsonResponse({"fields": list(fields)})


@require_GET
def categories_view(request):
    field_id, level, error = _parse_filters(request)
    if error:
        return error

    entries = _matching_entries(field_id, level)
    categories = (
        Category.objects.filter(entries__in=entries)
        .distinct()
        .order_by("order", "name")
        .values("id", "name")
    )
    return JsonResponse({"categories": list(categories)})


@require_GET
def questions_view(request):
    field_id, level, error = _parse_filters(request)
    if error:
        return error

    category_id = request.GET.get("category")
    if not category_id or not category_id.isdigit():
        return JsonResponse({"error": "دسته‌بندی معتبر نیست."}, status=400)

    entries = _matching_entries(field_id, level).filter(category_id=category_id)
    questions = entries.order_by("order", "-created_at").values("id", "question")
    return JsonResponse({"questions": list(questions)})


@require_GET
def question_detail_view(request, entry_id):
    entry = QAEntry.objects.filter(pk=entry_id, is_active=True).first()
    if entry is None:
        return JsonResponse({"error": "این سوال پیدا نشد."}, status=404)

    return JsonResponse({"id": entry.id, "question": entry.question, "answer": entry.answer})
