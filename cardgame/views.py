from django.shortcuts import redirect, render
from django.views import View
from . import forms
from django.contrib.auth import authenticate, login, logout

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
