# Generated by Django 2.2.7 on 2020-01-09 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20191226_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastermovie',
            name='Keywords',
            field=models.TextField(null=True),
        ),
    ]
