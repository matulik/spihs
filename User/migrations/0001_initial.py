# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Login')),
                ('password', models.CharField(max_length=100, unique=True, verbose_name='Password')),
                ('email', models.EmailField(max_length=254, verbose_name=b'E-mail')),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
