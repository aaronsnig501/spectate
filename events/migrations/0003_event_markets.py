# Generated by Django 3.1.4 on 2020-12-21 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0001_initial'),
        ('events', '0002_event_sport'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='markets',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='markets.market'),
            preserve_default=False,
        ),
    ]
