from django.urls import path
from . import views


urlpatterns = [
    path('novo_flashcard/', views.novo_flashcard, name="novo_flashcard"),
    path('delete_flashcard/<int:id>', views.delete_flashcard, name="delete_flashcard")
]

