from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

def cadastro(req):
    if req.method == 'GET':
        return render(req, 'cadastro.html')
    elif req.method == 'POST':
        nome = req.POST.get('nome')
        senha = req.POST.get('senha')
        c_senha = req.POST.get('confirmar_senha')
        if not senha == c_senha:
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=nome)
        if user.exists():
            return redirect('/usuarios/cadastro')

        try:
            User.objects.create_user(username=nome, password=senha)
            return redirect('/usuarios/login')
    
        except:
            return redirect('/usuarios/cadastro')
        
        
    
        return HttpResponse("success")