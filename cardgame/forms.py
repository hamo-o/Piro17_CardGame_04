from django import forms
from .models import User, Game
from django.contrib.auth.forms import UserCreationForm
import random

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise forms.ValidationError("비밀번호가 일치하지 않습니다!")
        except User.DoesNotExist:
            raise forms.ValidationError("해당 사용자가 존재하지 않습니다!")

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class AttackForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['attack_card', 'defender']

class DefendForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['defend_card']
