# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_auto_20160604_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordsStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5173\u952e\u5b57')),
                ('amount', models.IntegerField(blank=True, default=1, null=True, verbose_name='\u6570\u91cf')),
            ],
            options={
                'db_table': 'keywords',
                'verbose_name': '\u5173\u952e\u5b57',
                'verbose_name_plural': '\u5173\u952e\u5b57',
            },
        ),
        migrations.CreateModel(
            name='ScanOperatingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commented', models.FloatField(blank=True, default=0, null=True, verbose_name='\u5df2\u8bc4\u8bba')),
                ('liked', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u5df2\u70b9\u8d5e')),
                ('product_link_clicked', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u5df2\u70b9\u51fb\u5546\u54c1\u94fe\u63a5')),
            ],
            options={
                'db_table': 'scan_operating_Record',
                'verbose_name': '\u626b\u63cf\u540e\u64cd\u4f5c\u8bb0\u5f55',
                'verbose_name_plural': '\u626b\u63cf\u540e\u64cd\u4f5c\u8bb0\u5f55',
            },
        ),
        migrations.AddField(
            model_name='bundle',
            name='concerned_rate',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='\u4e13\u6ce8\u5ea6'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='feedback_rate',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='\u597d\u8bc4\u7387'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='product_link',
            field=models.TextField(blank=True, null=True, verbose_name='\u5546\u54c1\u94fe\u63a5'),
        ),
        migrations.AddField(
            model_name='comment',
            name='sentiment',
            field=models.FloatField(blank=True, null=True, verbose_name='\u60c5\u611f\u503c'),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='QRCode',
            field=models.ImageField(blank=True, default='QRCodes/qrcode.png', null=True, upload_to='QRCodes', verbose_name='\u4e8c\u7ef4\u7801'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='commentlocation',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='commentstatistics',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='scan',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='scanlocation',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AlterField(
            model_name='scanstatistics',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
        migrations.AddField(
            model_name='scanoperatingrecord',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle'),
        ),
        migrations.AddField(
            model_name='scanoperatingrecord',
            name='id_scan',
            field=models.ForeignKey(blank=True, db_column='id_Scan', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Scan', verbose_name='\u626b\u63cf\u8bb0\u5f55'),
        ),
        migrations.AddField(
            model_name='keywordsstatistics',
            name='id_bundle',
            field=models.ForeignKey(blank=True, db_column='id_Bundle', null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.Bundle', verbose_name='AR\u6a21\u578b'),
        ),
    ]
