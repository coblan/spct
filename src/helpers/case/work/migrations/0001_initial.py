# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-08 08:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import helpers.director.model_validator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organize', '0004_auto_20170608_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='new index', max_length=500, validators=[helpers.director.model_validator.has_str], verbose_name='name')),
                ('par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='work.Index', verbose_name='parent dir')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='new work', max_length=100, validators=[helpers.director.model_validator.has_str], verbose_name='\u540d\u79f0')),
                ('span', models.FloatField(default=0, help_text='\u5355\u4f4d(\u5c0f\u65f6)', verbose_name='\u5de5\u65f6')),
                ('status', models.CharField(choices=[('pass', '\u901a\u8fc7'), ('reject', '\u672a\u901a\u8fc7'), ('waiting', '\u7b49\u5f85\u5ba1\u6838')], default='waiting', max_length=20, verbose_name='\u72b6\u6001')),
                ('tag', models.CharField(blank=True, max_length=500, verbose_name='\u6807\u7b7e')),
                ('detail', models.TextField(blank=True, verbose_name='\u8be6\u7ec6')),
                ('desp_img', models.CharField(blank=True, max_length=300, verbose_name='\u63cf\u8ff0\u56fe\u7247')),
                ('par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='work.Index', verbose_name='\u76ee\u5f55')),
            ],
        ),
        migrations.CreateModel(
            name='WorkRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ex_span', models.FloatField(default=0, help_text='\u5355\u4f4d(\u5c0f\u65f6)\uff0c\u5c0f\u6570\u6216\u6574\u6570', verbose_name='\u8c03\u6574\u5de5\u65f6')),
                ('status', models.CharField(choices=[('pass', '\u901a\u8fc7'), ('reject', '\u672a\u901a\u8fc7'), ('waiting', '\u7b49\u5f85\u5ba1\u6838')], default='waiting', max_length=20, verbose_name='\u72b6\u6001')),
                ('short', models.CharField(blank=True, max_length=300, verbose_name='\u7b80\u77ed\u63cf\u8ff0')),
                ('detail', models.TextField(blank=True, verbose_name='\u8be6\u7ec6')),
                ('finish_time', models.CharField(default='', max_length=20, verbose_name='\u5b8c\u6210\u65f6\u95f4')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('desp_img', models.CharField(blank=True, max_length=300, verbose_name='\u63cf\u8ff0\u56fe\u7247')),
                ('count', models.IntegerField(default=1, help_text='\u6574\u6570', verbose_name='\u6570\u91cf')),
                ('check_depart', models.CharField(blank=True, max_length=200, verbose_name='\u5ba1\u6838\u90e8\u95e8\u7f16\u7801')),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organize.Employee', verbose_name='\u5458\u5de5')),
                ('work', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='work.Work', verbose_name='\u5de5\u65f6\u7c7b\u578b')),
            ],
        ),
    ]
