from django.shortcuts import redirect, render
from django.urls import is_valid_path
from django.views import View
from . import forms
from .models import User, Game
from django.contrib.auth import authenticate, login, logout
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

def game_rank(request):
    if request.user.is_authenticated:
        users = User.objects.all().order_by('point')
        
        context = {
            "users" : users
        }
        return render(request, 'cardgame/game_rank.html', context=context)
    else:
        return redirect("cardgame:main")
    
def defend(request, pk):
    game = Game.objects.get(pk = pk) 
    
    if request.method == "POST":
        form = forms.DefendForm(request.POST, instance=game)
        
        if form.is_valid():
            if game.attack_card == game.defend_card : #공격카드와 방어카드가 같은 수라면
                game.tie_flag = 1 #무승부 표시
            else :
                if game.game_mode == 'big_num' : #큰 수가 이기는 게임이라면
                    if game.attack_card > game.defend_card : #attacker가 이겼을 경우
                        game.victory_user = game.attacker
                        game.attacker.point += game.attack_card
                        game.defender.point -= game.defend_card
                    else : #defender가 이겼을 경우
                        game.victory_user = game.defender
                        game.attacker.point -= game.attack_card
                        game.defender.point += game.defend_card
                else : #작은 수가 이기는 게임이라면
                    if game.attack_card < game.defend_card : #attacker가 이겼을 경우
                        game.victory_user = game.attacker
                        game.attacker.point += game.attack_card
                        game.defender.point -= game.defend_card
                    else : #defender가 이겼을 경우
                        game.victory_user = game.defender
                        game.attacker.point -= game.attack_card
                        game.defender.point += game.defend_card
            game.game_status = 'end' #game_status를 'end'로 변경
            game.save() #game의 변경된 status 저장
            game.attacker.save() #attacker의 변경된 point 저장
            game.defender.save() #defender의 변경된 point 저장
            form.save()
            return redirect('/')
        else :
            return redirect('/')
    else :
        form = forms.DefendForm()
        context = {
            'form' : form,
            'game' : game
        }
        return render(request, 'cardgame/defend.html', context=context)

def game_detail(request, pk) :
    game = Game.objects.get(pk = pk)
    request_user = request.user
    
    context = {
        'game' : game,
        'request_user' : request_user
    }
    return render(request, 'cardgame/game_detail.html', context=context)

def game_list(request):
    game = Game.objects.all() 
    users = User.objects.all()
    end_attack_game = game.filter(
        attacker=request.user, game_status='end') #attacker의 게임이 끝났을 때
    proceed_attack_game = game.filter(
        attacker=request.user, game_status='proceed') #attacker의 게임이 진행 중일 때
    end_defend_game = game.filter(
        defender = request.user, game_status='end') #defender의 게임이 끝났을 때
    proceed_defend_game = game.filter(
        defender = request.user, game_status='proceed') #defender의 게임이 진행 중일 때

    end_games = end_attack_game.union(end_defend_game)
    proceed_games = proceed_attack_game.union(proceed_defend_game)

    context = {
        'end_games': end_games,
        'proceed_games': proceed_games,
        'current_user': request.user,
        'users':users
    }
    return render(request, 'cardgame/game_list.html', context=context)

def game_delete(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()
    return redirect("cardgame:game_list")
