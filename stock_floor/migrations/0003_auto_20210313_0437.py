# Generated by Django 3.1.6 on 2021-03-12 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_floor', '0002_auto_20210313_0300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='name',
        ),
    ]
