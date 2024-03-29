from django.shortcuts import render, redirect

from django.core.exceptions import ObjectDoesNotExist
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse, Http404


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
   
    card = Flashcard.objects.get(id=id)
    if not card.user == req.user:
        raise Http404()
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
            dificuldades=dificuldade,
        )

        desafio.save()

        for categoria in categorias:
            desafio.categoria.add(categoria)

        flashcards = (
            Flashcard.objects.filter(user=req.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by("?")
        )

        if flashcards.count() < int(q_perguntas):
            return redirect("/flashcard/iniciar_desafio")

        flashcards = flashcards[: int(q_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(flashcard=f)
            flashcard_desafio.save()
            desafio.flashcard.add(flashcard_desafio)

        desafio.save()

        return redirect('/flashcard/listar_desafio')


def listar_desafio(req,):  
    desafios = Desafio.objects.filter(user=req.user)
  
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    categorias = Categoria.objects.all()

    categoria = req.GET.get("categoria")
    dificuldade = req.GET.get("dificuldade")

    if categoria:
        desafios = desafios.filter(categoria__id=categoria)

    if dificuldade:
        desafios = desafios.filter(dificuldade=dificuldade)

    return render(
        req,
        "listar_desafio.html",
        {
            "desafios": desafios,
            "categorias": categorias,
            "dificuldades": dificuldades
        },
    )


def deletar_desafio(req, id):
    try:
        desafio = FlashcardDesafio.objects.get(id=id)
        print(desafio)
    except ObjectDoesNotExist:
        messages.add_message(req, constants.ERROR, "Desafio não encontrado!")
        return redirect('/flashcard/listar_desafio')

    if not desafio.user == req.user:
        raise Http404()
    print(desafio)
    desafio.delete()
    messages.add_message(req, constants.SUCCESS, "Desafio apagado com sucesso!")
    return redirect('/flashcard/listar_desafio')

def desafio(req, id):
    
    desafio = Desafio.objects.get(id=id)
    
    if not desafio.user == req.user:
        raise Http404()
    
    if req.method=="GET":
        acertos = desafio.flashcard.filter(respondido=True).filter(acertou=True).count()
        erros = desafio.flashcard.filter(respondido=True).filter(acertou=False).count()
        faltantes = desafio.flashcard.filter(respondido=False).count()
        return render(
            req,
            'desafio.html',
            {
                'desafio': desafio,
                'acertos': acertos,
                'erros': erros,
                'faltantes': faltantes
            }
        )


def responder_flashcard(req, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)
    acertou = req.GET.get('acertou')
    flashcard_desafio.respondido = True
    desafio_id = req.GET.get('desafio_id')
    '''
    if basico
    if acertou == "1":
        flashcard_desafio.acertou = True
    elif acertou == "0":
        flashcard_desafio.acertou = False'''
        
    #if avancado
    
    if not flashcard_desafio.flashcard.user == req.user:
        raise Http404
    
    flashcard_desafio.acertou = True if acertou == "1" else False
    flashcard_desafio.save()
    return redirect(f"/flashcard/desafio/{desafio_id}")


def relatorio(req, id):
    desafio = Desafio.objects.get(id=id)
    acertos = desafio.flashcard.filter(acertou=True).count()
    erros = desafio.flashcard.filter(acertou=False).count()
    dados = [acertos, erros]
    
    
    categorias = desafio.categoria.all()
    labels = []
    for i in categorias:
        labels.append(i.nome)
        
    dados2 = []
    for categoria in categorias:
        dados2.append(desafio.flashcard.filter(flashcard__categoria=categoria).filter(acertou=True).count())
        
    
    return render(req, 'relatorio.html', {'desafio': desafio, 'dados': dados, 'labels': labels, 'dados2': dados2})