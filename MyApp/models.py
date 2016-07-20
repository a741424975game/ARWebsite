# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

from MyApp.jieba_tags import *


class Bundle(models.Model):
    id_user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_User', blank=True, null=True,
                                verbose_name='用户名')  # Field name made lowercase.
    config_info = models.TextField(blank=True, null=True, verbose_name='AR模型的配置信息')
    QRCode = models.ImageField(blank=True, null=True, verbose_name='二维码', upload_to='QRCodes',
                               default='QRCodes/' + str(uuid.uuid1()) + 'qrcode.png')
    model = models.FileField(blank=True, null=True, verbose_name='模型文件', upload_to='bundles')
    imageTarget = models.ImageField(blank=True, null=True, verbose_name='AR显示目标图片', upload_to='imageTargets')
    name = models.TextField(blank=True, null=True, verbose_name='名字')
    likes = models.IntegerField(blank=True, null=True, verbose_name='点赞数量', default=0)
    scan_times = models.IntegerField(blank=True, null=True, verbose_name='扫描次数', default=0, )
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


class CommentStatistics(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    datetime = models.DateField(blank=True, null=True, verbose_name='时间', )
    amount = models.IntegerField(blank=True, null=True, verbose_name='数量', default=1)

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '评论数量统计'
        verbose_name_plural = verbose_name
        db_table = 'comment_statistics'


class Comment(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_location = models.ForeignKey('Locations', models.DO_NOTHING, db_column='id_Location', blank=True,
                                    null=True, verbose_name='地区')  # Field name made lowercase.
    content = models.TextField(blank=True, null=True, verbose_name='内容')
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='时间', auto_now_add=True)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        self.id_bundle.comments += 1
        self.id_bundle.save()
        tags = jieba_tags(self.content)
        for tag in tags:
            if KeywordsStatistics.objects.filter(id_bundle=self.id_bundle, keywords=tag):
                keywords_statistics = KeywordsStatistics.objects.get(id_bundle=self.id_bundle, keywords=tag)
                keywords_statistics.amount += 1
            else:
                keywords_statistics = KeywordsStatistics.objects.create(id_bundle=self.id_bundle, keywords=tag)
            keywords_statistics.save()
        if CommentStatistics.objects.filter(id_bundle=self.id_bundle, datetime=timezone.localtime(timezone.now())):
            comment_statistics = CommentStatistics.objects.get(id_bundle=self.id_bundle,
                                                               datetime=timezone.localtime(timezone.now()))
            comment_statistics.amount += 1
        else:
            comment_statistics = CommentStatistics.objects.create(id_bundle=self.id_bundle,
                                                                  datetime=timezone.localtime(timezone.now()))
        comment_statistics.save()
        if CommentLocation.objects.filter(id_bundle=self.id_bundle, id_location=self.id_location):
            comment_location = CommentLocation.objects.get(id_bundle=self.id_bundle, id_location=self.id_location)
            comment_location.amount += 1
        else:
            comment_location = CommentLocation.objects.create(id_bundle=self.id_bundle, id_location=self.id_location)
        comment_location.save()

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        db_table = 'comment'


class KeywordsStatistics(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')
    keywords = models.CharField(blank=True, null=True, max_length=30, verbose_name='关键字')
    amount = models.IntegerField(blank=True, null=True, default=1, verbose_name='数量')

    def __unicode__(self):
        return self.keywords

    class Meta:
        verbose_name = '关键字'
        verbose_name_plural = verbose_name
        db_table = 'keywords'


class CommentLocation(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_location = models.ForeignKey('Locations', models.DO_NOTHING, db_column='id_Location', blank=True,
                                    null=True, verbose_name='地区')  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True, verbose_name='数量', default=1)

    def __unicode__(self):
        return self.id_location.location

    class Meta:
        verbose_name = '评论的地理位置'
        verbose_name_plural = verbose_name
        db_table = 'comment_location'


class ScanStatistics(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    datetime = models.DateField(blank=True, null=True, verbose_name='时间')
    amount = models.IntegerField(blank=True, null=True, verbose_name='数量', default=1)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        print self.datetime

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '扫描数量统计'
        verbose_name_plural = verbose_name
        db_table = 'scan_statistics'


class Scan(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_location = models.ForeignKey('Locations', models.DO_NOTHING, db_column='id_Location', blank=True,
                                    null=True, verbose_name='地区')  # Field name made lowercase.
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='时间', auto_now_add=True)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        self.id_bundle.scan_times += 1
        self.id_bundle.save()
        if ScanStatistics.objects.filter(id_bundle=self.id_bundle, datetime=timezone.localtime(timezone.now())):
            scan_statistics = ScanStatistics.objects.get(id_bundle=self.id_bundle,
                                                         datetime=timezone.localtime(timezone.now()))
            scan_statistics.amount += 1
        else:
            scan_statistics = ScanStatistics.objects.create(id_bundle=self.id_bundle,
                                                            datetime=timezone.localtime(timezone.now()))
        scan_statistics.save()
        if ScanLocation.objects.filter(id_bundle=self.id_bundle, id_location=self.id_location):
            scan_location = ScanLocation.objects.get(id_bundle=self.id_bundle, id_location=self.id_location)
            scan_location.amount += 1
        else:
            scan_location = ScanLocation.objects.create(id_bundle=self.id_bundle, id_location=self.id_location)
        scan_location.save()

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '扫描记录'
        verbose_name_plural = verbose_name
        db_table = 'scan'


class ScanLocation(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_location = models.ForeignKey('Locations', models.DO_NOTHING, db_column='id_Location', blank=True,
                                    null=True, verbose_name='地区')  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True, verbose_name='数量', default=1)

    def __unicode__(self):
        return self.id_location.province + self.id_location.city + self.id_location.county

    class Meta:
        verbose_name = '扫描的地理位置'
        verbose_name_plural = verbose_name
        db_table = 'scan_location'


class Locations(models.Model):
    province = models.CharField(max_length=30, blank=True, null=True, verbose_name='省级')
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name='市级')
    county = models.CharField(max_length=30, blank=True, null=True, verbose_name='县级')

    def __unicode__(self):
            return self.province + self.city + self.county


    class Meta:
        verbose_name = '地理位置'
        verbose_name_plural = verbose_name
        db_table = 'location'
