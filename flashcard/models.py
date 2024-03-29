from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe



class Categoria(models.Model):
    nome = models.CharField(max_length=25)

    def __str__(self):
        return self.nome


class Flashcard(models.Model):
    DIFICULDADE_CHOICES = (("D", "Difícil"), ("M", "Médio"), ("F", "Fácil"))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pergunta = models.CharField(max_length=200)
    resposta = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)

    def __str__(self):
        return self.pergunta

    @property
    def css_dif(self):
        if self.dificuldade == "F":
            return "flashcard-facil"
        elif self.dificuldade == "M":
            return "flashcard-medio"
        elif self.dificuldade == "D":
            return "flashcard-dificil"


class FlashcardDesafio(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.DO_NOTHING)
    respondido = models.BooleanField(default=False)
    acertou = models.BooleanField(default=False)

    def __str__(self):
        return self.flashcard.pergunta


class Desafio(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    categoria = models.ManyToManyField(Categoria)
    q_perguntas = models.IntegerField()
    dificuldades = models.CharField(max_length=1, choices=Flashcard.DIFICULDADE_CHOICES)
    flashcard = models.ManyToManyField(FlashcardDesafio)

    def __str__(self):
        return self.titulo

    def status(self):
        if self.flashcard.filter(respondido=False).exists():
            return mark_safe('<span class="badge bg-primary">Em aberto</span>')
        else:
            return mark_safe('<span class="badge bg-success">Concluído</span>')