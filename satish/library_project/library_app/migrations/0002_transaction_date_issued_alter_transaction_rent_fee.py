# Generated by Django 4.2.5 on 2023-09-13 13:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date_issued',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='rent_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
