from django.urls import path, include 
from . import views

app_name = "cardgame"

urlpatterns = [
    path("", views.main, name="main"),
    path("defend/<int:pk>/", views.defend, name="defend"),
    path("game_detail/<int:pk>",views.game_detail, name="game_detail"),
    path("game_rank/", views.game_rank, name="game_rank"),
    path("game_list/", views.game_list, name="game_list"),
    path('game_delete/<int:pk>', views.game_delete, name='game_delete'),
    path("attack/", views.attack, name="attack"),
]
