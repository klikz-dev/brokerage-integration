# Generated by Django 5.0.7 on 2024-08-20 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetgroup',
            name='sort',
            field=models.IntegerField(default=0),
        ),
    ]
