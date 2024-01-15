from django.shortcuts import render
from django.http import HttpResponse

def cadastro(req):
    return render(req, 'cadastro.html')
