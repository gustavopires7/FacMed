# Generated by Django 5.1.1 on 2024-12-17 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_imagem_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='telefone_profissional',
            field=models.BooleanField(default=False, verbose_name='Este número é WhatsApp profissional?'),
        ),
    ]