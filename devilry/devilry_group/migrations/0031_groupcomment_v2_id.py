# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-06-30 10:12


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devilry_group', '0030_auto_20170621_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupcomment',
            name='v2_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
