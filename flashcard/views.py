from django.shortcuts import render, redirect
from .models import Categoria

def novo_flashcard(req):
    if not req.user.is_authenticated:
        return redirect("/usuarios/logar")
    elif req.method =="GET":
        categoria = Categoria.objects.all()
        return render(req, "novo_flashcard.html")
    