# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repostiroy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='capacity',
            field=models.CharField(max_length=32, verbose_name='磁盘容量GB'),
        ),
    ]
