# Generated by Django 4.2.3 on 2023-07-28 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='price',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]
