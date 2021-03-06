# Generated by Django 2.2.7 on 2019-12-26 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0008_auto_20191226_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Movie_ID', models.IntegerField()),
                ('User', models.TextField()),
                ('Vote', models.IntegerField()),
            ],
            options={
                'unique_together': {('Movie_ID', 'User')},
            },
        ),
        migrations.CreateModel(
            name='UserRecommendations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.TextField()),
                ('RecomLevel', models.IntegerField()),
                ('Movie_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.MasterMovie')),
            ],
            options={
                'unique_together': {('Movie_FK', 'User')},
            },
        ),
    ]
