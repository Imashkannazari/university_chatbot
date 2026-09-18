from django.urls import path

from . import views

urlpatterns = [
    path("fields/", views.fields_view, name="fields"),
    path("categories/", views.categories_view, name="categories"),
    path("questions/", views.questions_view, name="questions"),
    path("questions/<int:entry_id>/", views.question_detail_view, name="question-detail"),
]
