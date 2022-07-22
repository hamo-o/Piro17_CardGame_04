# Generated by Django 4.0.6 on 2022-07-22 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardgame', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='tie_flag',
        ),
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(choices=[('end', 'end'), ('proceed', 'proceed')], max_length=20),
        ),
    ]