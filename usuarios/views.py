from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


def cadastro(req):
    if req.method == "GET":
        return render(req, "cadastro.html")
    elif req.method == "POST":
        nome = req.POST.get("nome")
        senha = req.POST.get("senha")
        c_senha = req.POST.get("confirmar_senha")

        if not senha == c_senha:
            messages.add_message(
                req, constants.ERROR, "Senha e Confirmar senha não coincidem."
            )
            return redirect("/usuarios/cadastro")

        user = User.objects.filter(username=nome)
        if user.exists():
            messages.add_message(req, constants.ERROR, "Nome já existe!! ")
            return redirect("/usuarios/cadastro")

        try:
            User.objects.create_user(username=nome, password=senha)
            return redirect("/usuarios/logar")

        except:
            messages.add_message(req, constants.ERROR, "Erro interno do Server.")
            return redirect("/usuarios/cadastro")


def logar(req):
    if req.method == "GET":
        return render(req, "login.html")
    elif req.method == "POST":
        nome = req.POST.get("nome")
        senha = req.POST.get("senha")

        user = auth.authenticate(req, username=nome, password=senha)
        
        if user:
            auth.login(req, user)
            messages.add_message(req, constants.SUCCESS, "Logado!")
            return redirect('/flashcard/novo_flashcard/')
        else:
            messages.add_message(req, constants.ERROR, "Usuário ou senha incorreto.")
            return redirect("/usuarios/logar")
        
def sair(req):
    auth.logout(req)
    return redirect('/usuarios/logar/')       
        
        
        
        