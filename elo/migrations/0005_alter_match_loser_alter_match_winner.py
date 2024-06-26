# Generated by Django 5.0.3 on 2024-03-29 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elo', '0004_alter_elo_image_alter_elo_n_games_alter_elo_n_losses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='losses', to='elo.elo'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='wins', to='elo.elo'),
        ),
    ]
