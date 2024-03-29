from django.urls import path
from . import views


urlpatterns = [
    path('novo_flashcard/', views.novo_flashcard, name="novo_flashcard"),
    path('delete_flashcard/<int:id>', views.delete_flashcard, name="delete_flashcard"),
    path('iniciar_desafio/', views.iniciar_desafio, name="iniciar_desafio"),
    path('listar_desafio/', views.listar_desafio, name='listar_desafio'),
    path('deletar_desafio/<int:id>', views.deletar_desafio, name="deletar_desafio"),
    path('desafio/<int:id>/', views.desafio, name='desafio'),
    path('responder_flashcard/<int:id>/', views.responder_flashcard, name="responder_flashcard"),
    path('relatorio/<int:id>/', views.relatorio, name='relatorio')
]

