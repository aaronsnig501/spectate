# Generated by Django 3.1.4 on 2020-12-27 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]