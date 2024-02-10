from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Apostila, ViewApostila, Tags
from django.contrib.messages import constants
from django.contrib import messages

def add_apostila(req):
    if req.method == "GET":
        apostilas = Apostila.objects.filter(user=req.user)
        views_totais = ViewApostila.objects.filter(apostila__user=req.user).count()
        
        return render(req, 'add_apostila.html', {'apostilas': apostilas, 'views_totais': views_totais})
    
    elif req.method == "POST":
        titulo = req.POST.get('titulo')
        arquivo = req.FILES['arquivo']
        
        apostila = Apostila(
            user=req.user,
            titulo=titulo,
            arquivo=arquivo,
           
        )
        apostila.save()
        tags = req.POST.get('tags')
        list_tags = tags.split(',')
        
        for tag in list_tags:
            nova_tag = Tags(
                nome=tag
            )
            nova_tag.save()
            apostila.tags.add(nova_tag)
            
        
        apostila.save()
        
        messages.add_message(req, constants.SUCCESS, message='Salvo com sucesso!')
        return redirect('/apostila/add_apostila')
        
def apostila(req, id):
    apostila = Apostila.objects.get(id=id)
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()
    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    
    view = ViewApostila(
        ip=req.META['REMOTE_ADDR'],
        apostila=apostila
    )
    view.save()
    return render(req, 'apostila.html', {'apostila': apostila, 'views_totais': views_totais, 'views_unicas': views_unicas})
        