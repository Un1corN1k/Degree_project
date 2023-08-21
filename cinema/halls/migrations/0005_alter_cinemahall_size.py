# Generated by Django 4.2.3 on 2023-08-21 12:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0004_remove_moviesession_reserved_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinemahall',
            name='size',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(5)]),
        ),
    ]
