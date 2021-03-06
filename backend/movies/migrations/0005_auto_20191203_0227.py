# Generated by Django 2.2.7 on 2019-12-03 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20191126_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imdb_load',
            name='Duration',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='UserRecommendations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.TextField()),
                ('RecLevel', models.IntegerField()),
                ('Movie_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.MasterMovie')),
            ],
        ),
    ]
