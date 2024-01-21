from django.shortcuts import render, redirect

def home(req):
    return redirect("/usuarios/cadastro")
