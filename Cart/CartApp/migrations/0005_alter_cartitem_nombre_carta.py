# Generated by Django 4.2.3 on 2023-09-10 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CartApp', '0004_cartitem_nombre_carta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='nombre_carta',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
