# Generated by Django 3.2.13 on 2023-01-31 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0014_use_autofields_for_pk'),
        ('core', '0002_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='calendar',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.calendar'),
        ),
    ]
