from django.shortcuts import render, redirect
from .models import Categoria, Flashcard
from django.contrib.messages import constants
from django.contrib import messages

def novo_flashcard(req):
    if not req.user.is_authenticated:
        return redirect("/usuarios/logar")
    elif req.method =="GET":
        categoria = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=req.user)
        
        categoria_filter = req.GET.get('categoria')
        dificuldade_filter = req.GET.get('dificuldade')
        
        if categoria_filter:
            flashcards = flashcards.filter(categoria__id=categoria_filter)
        
        if dificuldade_filter:
            flashcards = flashcards.filter(dificuldade=dificuldade_filter)
        
        return render(req, "novo_flashcard.html", {'categorias': categoria, 'dificuldades': dificuldades, 'flashcards': flashcards})
    elif req.method =="POST":
        pergunta = req.POST.get('pergunta')
        resposta = req.POST.get('resposta')
        categoria = req.POST.get('categoria')
        dificuldade = req.POST.get('dificuldade')
        
        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(req, constants.ERROR, "Preencha os campos de pergunta e resposta.")
            return redirect("/flashcard/novo_flashcard/")
        
        
        flashcard = Flashcard(
            user=req.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade
        )
        
        flashcard.save()
        messages.add_message(req, constants.SUCCESS, "Flashcard cadastrado com sucesso!")
        return redirect('/flashcard/novo_flashcard/')
    
    
    
    
def delete_flashcard(req, id):
    card = Flashcard.objects.get(id=id)
    card.delete()
    messages.add_message(req, constants.SUCCESS, "Flashcard apagado com sucesso!")
    return redirect('/flashcard/novo_flashcard/')
    
    