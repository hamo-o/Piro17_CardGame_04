from secrets import choice
from django.shortcuts import redirect, render
from django.urls import is_valid_path
from django.views import View
from . import forms
from .models import User #?
from .models import User, Game
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
import random


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        context = {
            "form" : form
        }
        return render(request, "cardgame/login.html", context)

    def post(self, request):
        form = forms.LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username = username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("cardgame:main")

        context = {
            "form" : form
        }
        return render(request, "cardgame/login.html", context)
# Create your views here.
def main (request):
    return render(request, "cardgame/main.html")

def sign_up(request):
    if request.method == "POST":
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("cardgame:main")

        return redirect("cardgame:sign_up")

    else:
        form = forms.SignupForm()
        context = {
            "form" : form
        }
        return render(request, "cardgame/sign_up.html", context)

def log_out(request):
    logout(request)
    return redirect("cardgame:main")

def defend(request):
    if request.method == "POST":
        form = forms.DefendForm(request.POST)
        
        if form.is_valid():
            defend = form.save()
            defend.user = request.user
            defend.save()
            return redirect('/')
        else :
            return redirect('/')
    else :
        form = forms.DefendForm()
        context = {
            'form' : form
        }
        return render(request, 'cardgame/defend.html', context=context)


def attack(request):
    games = Game.objects.all()

    if request.method == 'POST':
        form = forms.AttackForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.attacker = request.user
            game.game_mode=random.choice(['big_num', 'small_num'])
            game.game_status='proceed'
            game.save()
            return redirect('game_list/')
        else :
            return redirect('game_list/')
    else :
        form = forms.AttackForm()
        user = get_user_model()
        form = forms.AttackForm()
        form.fields['defender'].queryset = user.objects.all().exclude(id=request.user.id)
        context={
            'form':form,
            'games':games,
        }
        return render(request, 'cardgame/attack.html', context=context)



