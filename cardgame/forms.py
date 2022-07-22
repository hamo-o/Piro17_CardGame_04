from django import forms
from .models import User, Game
from django.contrib.auth.forms import UserCreationForm
import random

class AttackForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['attack_card', 'defender']

class DefendForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['defend_card']
