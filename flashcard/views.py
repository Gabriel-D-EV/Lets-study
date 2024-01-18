from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse



def novo_flashcard(req):
    if not req.user.is_authenticated:
        return redirect("/usuarios/logar")
    elif req.method == "GET":
        categoria = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=req.user)

        categoria_filter = req.GET.get("categoria")
        dificuldade_filter = req.GET.get("dificuldade")

        if categoria_filter:
            flashcards = flashcards.filter(categoria__id=categoria_filter)

        if dificuldade_filter:
            flashcards = flashcards.filter(dificuldade=dificuldade_filter)

        return render(
            req,
            "novo_flashcard.html",
            {
                "categorias": categoria,
                "dificuldades": dificuldades,
                "flashcards": flashcards,
            },
        )
    elif req.method == "POST":
        pergunta = req.POST.get("pergunta")
        resposta = req.POST.get("resposta")
        categoria = req.POST.get("categoria")
        dificuldade = req.POST.get("dificuldade")

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                req, constants.ERROR, "Preencha os campos de pergunta e resposta."
            )
            return redirect("/flashcard/novo_flashcard/")

        flashcard = Flashcard(
            user=req.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        flashcard.save()
        messages.add_message(
            req, constants.SUCCESS, "Flashcard cadastrado com sucesso!"
        )
        return redirect("/flashcard/novo_flashcard/")


def delete_flashcard(req, id):
    if not req.user.is_authenticated:
        return redirect("/usuarios/logar")
    else:
        card = Flashcard.objects.get(id=id)
        card.delete()
        messages.add_message(req, constants.SUCCESS, "Flashcard apagado com sucesso!")
        return redirect("/flashcard/novo_flashcard/")


def iniciar_desafio(req):
    if req.method == "GET":
        categoria = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(
            req,
            "iniciar_desafio.html",
            {
                "categorias": categoria,
                "dificuldades": dificuldades,
            },
        )

    elif req.method == "POST":
        titulo = req.POST.get("titulo")
        categorias = req.POST.getlist("categoria")
        dificuldade = req.POST.get("dificuldade")
        q_perguntas = req.POST.get("q_perguntas")

        desafio = Desafio(
            user=req.user,
            titulo=titulo,
            q_perguntas=q_perguntas,
            dificuldades=dificuldade
        )

        desafio.save()

        for categoria in categorias:
            desafio.categoria.add(categoria)

        flashcards = (
            Flashcard.objects.filter(user=req.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by('?')
        )
        
        print(len(flashcards))
        #flashcards = flashcards[: int(q_perguntas)]

        return HttpResponse('teste')
