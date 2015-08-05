# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import User.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=User.models.defaultToken, max_length=32)),
                ('dateCreate', models.DateTimeField(default=datetime.datetime(2015, 8, 5, 13, 33, 51, 685222, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Login')),
                ('password', models.CharField(max_length=100, unique=True, verbose_name='Password')),
                ('email', models.EmailField(max_length=254, verbose_name=b'E-mail')),
                ('status', models.IntegerField(default=0)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Token')),
            ],
        ),
    ]
