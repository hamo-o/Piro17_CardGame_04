# Generated by Django 4.0.6 on 2022-07-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardgame', '0003_alter_game_game_mode_alter_game_game_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(choices=[('end', 'end'), ('proceed', 'proceed')], max_length=20),
        ),
    ]