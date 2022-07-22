from django.shortcuts import redirect, render
from django.urls import is_valid_path
from django.views import View
from . import forms
from .models import User, Game
from django.contrib.auth import authenticate, login, logout
import random
from django import forms as f

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

        return render(request, "cardgame/sign_up.html", {'form':form})

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

def MakeRandomCard():
    choice_list=[('','----')]
    num_list = random.sample([1,2,3,4,5,6,7,8,9,10], 5)
    for num in num_list:
        temp = []
        temp.append(num)
        temp.append(num)
        temp = tuple(temp)
        choice_list.append(temp)
    choice_list=tuple(choice_list)
    return choice_list

def defend(request, pk):
    random_choices = MakeRandomCard() #랜덤 숫자 목록 생성

    game = Game.objects.get(pk = pk) 
    
    #DefendForm의 choices에 랜덤으로 생성된 숫자 목록을 할당한다
    form = forms.DefendForm()
    form.fields['defend_card'] = f.ChoiceField(choices=random_choices, label="내가 고른 카드")
    
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
                        
            defend = form.save(commit=False)
            defend.game_status = 'end' #game_status를 'end'로 변경
            defend.attacker.save()
            defend.defender.save()
            defend.save()

            return redirect('/game_detail/'+str(pk))
        else :
            print('invalid form error')
            return redirect('/')
    else :
        context = {
            'form' : form,
            'game' : game,
            'pk' : str(pk)
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
    attack_game = game.filter(attacker=request.user) 
    defend_game = game.filter(defender = request.user)

    games = attack_game.union(defend_game) #전체 게임
    status_proceed = game.filter(game_status = 'proceed') #진행 중인 상태인 게임
    stauts_end = game.filter(game_status = 'end') #완료된 상태인 게임
    context = {
        'status_proceed' : status_proceed,
        'stauts_end' : stauts_end,
        'games' : games,
        'current_user': request.user,
        'users':users
    }
    return render(request, 'cardgame/game_list.html', context=context)

def game_delete(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()
    return redirect("cardgame:game_list")
