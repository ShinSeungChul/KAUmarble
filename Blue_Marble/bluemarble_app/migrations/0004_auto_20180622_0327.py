# Generated by Django 2.0.6 on 2018-06-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluemarble_app', '0003_auto_20180622_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='num',
            field=models.IntegerField(),
        ),
    ]
