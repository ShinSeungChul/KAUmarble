# Generated by Django 2.0.6 on 2018-06-09 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluemarble_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roominfo',
            name='countOfVictory1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='roominfo',
            name='countOfVictory2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='roominfo',
            name='major1',
            field=models.CharField(default='none', max_length=10),
        ),
        migrations.AddField(
            model_name='roominfo',
            name='major2',
            field=models.CharField(default='none', max_length=10),
        ),
    ]
