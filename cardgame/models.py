from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  point = models.IntegerField(default=0)

MODE_CHOICE = {('big_num', 'big_num'),('small_num', 'small_num')}
STATUS_CHOICE = {('proceed', 'proceed'),('end', 'end')}
class Game(models.Model):
  attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attacker")
  defenser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="defenser")
  attack_card = models.IntegerField()
  defense_card = models.IntegerField()
  game_mode = models.CharField(max_length=20, choices=MODE_CHOICE)
  game_status = models.CharField(max_length=20, choices=STATUS_CHOICE)
  victory_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)