# Generated by Django 2.0.1 on 2018-01-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20180116_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read_time',
            field=models.IntegerField(default=0),
        ),
    ]