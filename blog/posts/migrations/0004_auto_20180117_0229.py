# Generated by Django 2.0.1 on 2018-01-17 02:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 17, 2, 29, 43, 598504, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
