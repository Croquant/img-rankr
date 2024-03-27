# Generated by Django 5.0.3 on 2024-03-27 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elo', '0002_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='losses', to='elo.elo'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wins', to='elo.elo'),
        ),
    ]
