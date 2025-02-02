# Generated by Django 3.0.8 on 2020-09-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloks',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('bk_title', models.CharField(max_length=32)),
                ('bk_describe', models.CharField(max_length=64)),
                ('bk_text', models.CharField(max_length=2048)),
                ('bk_author', models.CharField(max_length=32)),
                ('bk_love', models.IntegerField()),
                ('bk_time', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('tk_bk', models.IntegerField()),
                ('tk_author', models.CharField(max_length=32)),
                ('tk_text', models.CharField(max_length=128)),
                ('tk_time', models.CharField(max_length=32)),
            ],
        ),
    ]
