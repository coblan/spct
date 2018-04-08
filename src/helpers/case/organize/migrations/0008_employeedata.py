# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-20 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organize', '0007_workpermitmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='content')),
                ('emp', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organize.Employee', verbose_name='employee')),
            ],
        ),
    ]
