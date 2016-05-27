# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Bundle(models.Model):
    id_user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_User', blank=True, null=True,
                                verbose_name='用户名')  # Field name made lowercase.
    config_info = models.TextField(blank=True, null=True, verbose_name='AR模型的配置信息')
    QRCode = models.ImageField(blank=True, null=True, verbose_name='二维码', upload_to='./uploads/QRCodes')
    model = models.FileField(blank=True, null=True, verbose_name='模型文件', upload_to='./uploads/bundles')
    imageTarget = models.ImageField(blank=True, null=True, verbose_name='AR显示目标图片', upload_to='./uploads/imageTargets')
    name = models.TextField(blank=True, null=True, verbose_name='名字')
    likes = models.IntegerField(blank=True, null=True, verbose_name='点赞数量', default=0)
    scan_times = models.IntegerField(blank=True, null=True, verbose_name='扫描次数', default=0)
    comments = models.IntegerField(blank=True, null=True, verbose_name='评论数', default=0)
    upload_datetime = models.DateTimeField(blank=True, null=True, verbose_name='上传时间', auto_now_add=True)
    last_edit_datetime = models.DateTimeField(blank=True, null=True, verbose_name='最后一次编辑时间', auto_now=True)
    note = models.TextField(blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'AR模型'
        verbose_name_plural = verbose_name
        db_table = 'bundle'


class Comment(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_comment_location = models.ForeignKey('CommentLocation', models.DO_NOTHING, db_column='id_Comment_Location',
                                            blank=True, null=True, verbose_name='地区')  # Field name made lowercase.
    content = models.TextField(blank=True, null=True, verbose_name='内容')
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='时间', auto_now_add=True)

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        db_table = 'comment'


class CommentLocation(models.Model):
    location = models.TextField(db_column='Location', blank=True, null=True,
                                verbose_name='地区')  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True, verbose_name='数量', default=1)

    def __unicode__(self):
        return self.location

    class Meta:
        verbose_name = '评论的地理位置'
        verbose_name_plural = verbose_name
        db_table = 'comment_location'


class Scan(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_scan_location = models.ForeignKey('ScanLocation', models.DO_NOTHING, db_column='id_Scan_Location', blank=True,
                                         null=True, verbose_name='地区')  # Field name made lowercase.
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='时间', auto_now_add=True)

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '扫描记录'
        verbose_name_plural = verbose_name
        db_table = 'scan'


class ScanLocation(models.Model):
    location = models.TextField(db_column='Location', blank=True, null=True,
                                verbose_name='地区')  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True, verbose_name='数量', default=1)

    def __unicode__(self):
        return self.location

    class Meta:
        verbose_name = '扫描的地理位置'
        verbose_name_plural = verbose_name
        db_table = 'scan_location'
