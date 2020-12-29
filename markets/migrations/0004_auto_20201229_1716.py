# Generated by Django 3.1.4 on 2020-12-29 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0003_sport_number_of_participants'),
        ('markets', '0003_market_sport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markets', to='sports.sport'),
        ),
    ]