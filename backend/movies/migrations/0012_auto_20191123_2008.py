# Generated by Django 2.2.7 on 2019-11-23 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_auto_20191123_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedb_load',
            name='Poster',
            field=models.TextField(null=True),
        ),
    ]
