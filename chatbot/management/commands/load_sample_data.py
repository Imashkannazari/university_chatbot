from django.core.management.base import BaseCommand

from chatbot.models import Category, Field, QAEntry

FIELDS = [
    "مهندسی کامپیوتر",
    "مهندسی برق",
    "حسابداری",
    "روانشناسی",
]

CATEGORIES = ["ثبت‌نام", "شهریه", "پیش‌نیاز دروس", "چارت درسی", "فارغ‌التحصیلی"]

# هر ردیف: (دسته‌بندی، رشته یا None برای عمومی، مقطع یا "" برای عمومی، سوال، جواب)
ENTRIES = [
    # سوالات عمومی - برای همه رشته‌ها و همه مقاطع
    (
        "ثبت‌نام",
        None,
        "",
        "زمان ثبت‌نام ترم جدید چه موقع است؟",
        "ثبت‌نام هر ترم معمولاً یک هفته قبل از شروع کلاس‌ها از طریق سامانه آموزشی دانشگاه انجام می‌شود. "
        "تاریخ دقیق هر ترم در اطلاعیه‌های آموزش اعلام می‌گردد.",
    ),
    (
        "شهریه",
        None,
        "",
        "شهریه ثابت هر ترم چقدر است؟",
        "مبلغ شهریه ثابت هر ترم بر اساس مصوبه هیئت امنا تعیین می‌شود و از طریق سامانه مالی دانشجویی قابل مشاهده است.",
    ),
    (
        "فارغ‌التحصیلی",
        None,
        "",
        "برای دریافت مدرک فارغ‌التحصیلی چه مراحلی باید طی شود؟",
        "پس از گذراندن تمام واحدهای درسی، باید فرم تسویه‌حساب را از طریق سامانه آموزشی تکمیل و به اداره فارغ‌التحصیلان "
        "تحویل دهید. صدور مدرک معمولاً چند هفته پس از تسویه کامل انجام می‌شود.",
    ),
    # سوالات اختصاصی مهندسی کامپیوتر
    (
        "پیش‌نیاز دروس",
        "مهندسی کامپیوتر",
        "karshenasi",
        "پیش‌نیاز درس ساختمان داده چیست؟",
        "برای اخذ درس ساختمان داده باید درس برنامه‌سازی پیشرفته را با نمره قبولی گذرانده باشید.",
    ),
    (
        "چارت درسی",
        "مهندسی کامپیوتر",
        "karshenasi",
        "چارت درسی رشته مهندسی کامپیوتر کجا موجود است؟",
        "چارت درسی کامل رشته مهندسی کامپیوتر در سایت آموزش دانشکده فنی، بخش «چارت‌های درسی»، "
        "به تفکیک ورودی هر سال قرار دارد.",
    ),
    # سوال اختصاصی مقطع کارشناسی ارشد (برای همه رشته‌ها)
    (
        "فارغ‌التحصیلی",
        None,
        "arshad",
        "دفاع از پایان‌نامه چه شرایطی دارد؟",
        "برای دفاع از پایان‌نامه باید حداقل یک مقاله مستخرج از پایان‌نامه ارسال یا پذیرفته شده باشد و "
        "استاد راهنما تأییدیه آمادگی دفاع را صادر کند.",
    ),
    # سوال اختصاصی حسابداری
    (
        "پیش‌نیاز دروس",
        "حسابداری",
        "karshenasi",
        "پیش‌نیاز درس حسابداری میانه ۲ چیست؟",
        "برای اخذ درس حسابداری میانه ۲ باید درس حسابداری میانه ۱ را با نمره قبولی گذرانده باشید.",
    ),
]


class Command(BaseCommand):
    help = "چند رشته، دسته‌بندی و سوال‌جواب نمونه برای تست ویزارد اضافه می‌کند."

    def handle(self, *args, **options):
        field_objs = {}
        for i, name in enumerate(FIELDS):
            field, _ = Field.objects.get_or_create(name=name, defaults={"order": i})
            field_objs[name] = field

        category_objs = {}
        for i, name in enumerate(CATEGORIES):
            category, _ = Category.objects.get_or_create(name=name, defaults={"order": i})
            category_objs[name] = category

        created_count = 0
        for category_name, field_name, level, question, answer in ENTRIES:
            _, created = QAEntry.objects.get_or_create(
                question=question,
                defaults={
                    "answer": answer,
                    "category": category_objs[category_name],
                    "field": field_objs.get(field_name) if field_name else None,
                    "level": level,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(field_objs)} رشته، {len(category_objs)} دسته‌بندی و "
                f"{created_count} سوال‌جواب نمونه اضافه شد."
            )
        )
