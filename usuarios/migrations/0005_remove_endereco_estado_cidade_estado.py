# Generated by Django 5.1.4 on 2024-12-11 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuario_telefone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endereco',
            name='estado',
        ),
        migrations.AddField(
            model_name='cidade',
            name='estado',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.estado'),
        ),
    ]
