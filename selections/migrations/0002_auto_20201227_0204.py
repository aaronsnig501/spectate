# Generated by Django 3.1.4 on 2020-12-27 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selection',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
