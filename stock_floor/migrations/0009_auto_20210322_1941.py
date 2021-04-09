# Generated by Django 3.1.7 on 2021-03-22 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_floor', '0008_delete_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='stock_floor.comment'),
        ),
    ]
