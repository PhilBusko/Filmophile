# Generated by Django 2.2.7 on 2019-11-26 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20191126_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imdb_load',
            name='GrossUs',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='imdb_load',
            name='GrossWorldwide',
            field=models.TextField(null=True),
        ),
    ]