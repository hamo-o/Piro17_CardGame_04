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

class AttackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttackForm, self).__init__(*args, **kwargs)
        self.fields['attack_card'] = forms.ChoiceField(choices=MakeRandomCard(), label="내가 고른 카드")
    class Meta:
        model = Game
        fields = ['attack_card', 'defender']

class DefendForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DefendForm, self).__init__(*args, **kwargs)
        self.fields['defend_card'] = forms.ChoiceField(choices=MakeRandomCard(), label="내가 고른 카드")
    class Meta:
        model = Game
        fields = ['defend_card']
