# Generated by Django 3.1.4 on 2020-12-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0002_auto_20201227_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='sport',
            name='number_of_participants',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
