# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-24 15:04


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devilry_group', '0024_auto_20170107_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackset',
            name='feedbackset_type',
            field=models.CharField(choices=[('first_attempt', 'first attempt'), ('new_attempt', 'new attempt'), ('re_edit', 're edit'), ('merge_first_attempt', 'merge first attempt'), ('merge_new_attempt', 'merge new attempt'), ('merge_re_edit', 'merge re edit')], db_index=True, default='new_attempt', max_length=50),
        ),
    ]
