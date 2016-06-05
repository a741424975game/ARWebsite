# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 08:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateField(blank=True, null=True, verbose_name='\u65f6\u95f4')),
                ('amount', models.IntegerField(blank=True, default=1, null=True, verbose_name='\u6570\u91cf')),
            ],
            options={
                'db_table': 'comment_statistics',
                'verbose_name': '\u8bc4\u8bba\u6570\u91cf\u7edf\u8ba1',
                'verbose_name_plural': '\u8bc4\u8bba\u6570\u91cf\u7edf\u8ba1',
            },
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u7701\u7ea7')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5e02\u7ea7')),
                ('county', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u53bf\u7ea7')),
            ],
            options={
                'db_table': 'location',
                'verbose_name': '\u5730\u7406\u4f4d\u7f6e',
                'verbose_name_plural': '\u5730\u7406\u4f4d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='ScanStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateField(blank=True, null=True, verbose_name='\u65f6\u95f4')),
                ('amount', models.IntegerField(blank=True, default=1, null=True, verbose_name='\u6570\u91cf')),
            ],
            options={
                'db_table': 'scan_statistics',
                'verbose_name': '\u626b\u63cf\u6570\u91cf\u7edf\u8ba1',
                'verbose_name_plural': '\u626b\u63cf\u6570\u91cf\u7edf\u8ba1',
            },
        ),
        migrations.AlterModelOptions(
            name='bundle',
            options={'verbose_name': 'AR\u6a21\u578b', 'verbose_name_plural': 'AR\u6a21\u578b'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '\u8bc4\u8bba', 'verbose_name_plural': '\u8bc4\u8bba'},
        ),
        migrations.AlterModelOptions(
            name='commentlocation',
            options={'verbose_name': '\u8bc4\u8bba\u7684\u5730\u7406\u4f4d\u7f6e', 'verbose_name_plural': '\u8bc4\u8bba\u7684\u5730\u7406\u4f4d\u7f6e'},
        ),
        migrations.AlterModelOptions(
            name='scan',
            options={'verbose_name': '\u626b\u63cf\u8bb0\u5f55', 'verbose_name_plural': '\u626b\u63cf\u8bb0\u5f55'},
        ),
        migrations.AlterModelOptions(
            name='scanlocation',
            options={'verbose_name': '\u626b\u63cf\u7684\u5730\u7406\u4f4d\u7f6e', 'verbose_name_plural': '\u626b\u63cf\u7684\u5730\u7406\u4f4d\u7f6e'},
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='datetime',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='like',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='url',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='id_comment_location',
        ),
        migrations.RemoveField(
            model_name='commentlocation',
            name='location',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='id_scan_location',
        ),
        migrations.RemoveField(
            model_name='scanlocation',
            name='location',
        ),
        migrations.AddField(
            model_name='bundle',
            name='QRCode',
            field=models.ImageField(blank=True, default='QRCodes/b2746af3-2a2b-11e6-a7ce-ac87a316b12fqrcode.png', null=True, upload_to='QRCodes', verbose_name='\u4e8c\u7ef4\u7801'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='comments',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='\u8bc4\u8bba\u6570'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='config_info',
            field=models.TextField(blank=True, null=True, verbose_name='AR\u6a21\u578b\u7684\u914d\u7f6e\u4fe1\u606f'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='imageTarget',
            field=models.ImageField(blank=True, null=True, upload_to='imageTargets', verbose_name='AR\u663e\u793a\u76ee\u6807\u56fe\u7247'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='last_edit_datetime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='\u6700\u540e\u4e00\u6b21\u7f16\u8f91\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='\u70b9\u8d5e\u6570\u91cf'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='model',
            field=models.FileField(blank=True, null=True, upload_to='bundles', verbose_name='\u6a21\u578b\u6587\u4ef6'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='upload_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u4e0a\u4f20\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='commentlocation',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AddField(
            model_name='scan',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='scanlocation',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='id_user',
            field=models.ForeignKey(blank=True, db_column='id_User', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237\u540d'),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='name',
            field=models.TextField(blank=True, null=True, verbose_name='\u540d\u5b57'),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='scan_times',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='\u626b\u63cf\u6b21\u6570'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='commentlocation',
            name='amount',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='\u6570\u91cf'),
        ),
        migrations.AlterField(
            model_name='scan',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='scanlocation',
            name='amount',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='\u6570\u91cf'),
        ),
        migrations.AddField(
            model_name='scanstatistics',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AddField(
            model_name='commentstatistics',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AddField(
            model_name='comment',
            name='id_location',
            field=models.ForeignKey(blank=True, db_column='id_Location', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Locations', verbose_name='\u5730\u533a'),
        ),
        migrations.AddField(
            model_name='commentlocation',
            name='id_location',
            field=models.ForeignKey(blank=True, db_column='id_Location', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Locations', verbose_name='\u5730\u533a'),
        ),
        migrations.AddField(
            model_name='scan',
            name='id_location',
            field=models.ForeignKey(blank=True, db_column='id_Location', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Locations', verbose_name='\u5730\u533a'),
        ),
        migrations.AddField(
            model_name='scanlocation',
            name='id_location',
            field=models.ForeignKey(blank=True, db_column='id_Location', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MyApp.Locations', verbose_name='\u5730\u533a'),
        ),
    ]