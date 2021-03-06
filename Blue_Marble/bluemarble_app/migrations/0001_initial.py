# Generated by Django 2.0.6 on 2018-06-02 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.TextField(max_length=200)),
                ('room_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RoomInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('full', models.IntegerField(default=0)),
                ('user1', models.CharField(default='none', max_length=15)),
                ('user2', models.CharField(default='none', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='RoomMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('major', models.CharField(max_length=10)),
                ('countOfVictory', models.IntegerField(default=0)),
            ],
        ),
    ]
