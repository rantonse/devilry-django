# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-02 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devilry_compressionutil', '0006_compressedarchivemeta_created_by_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compressedarchivemeta',
            name='archive_size',
            field=models.BigIntegerField(),
        ),
    ]