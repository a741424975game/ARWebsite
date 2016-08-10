# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import threading
import uuid
from snownlp import SnowNLP

from MyApp.jieba_tags import *
from ARWebsite.settings import CONCERNED_THRESHOLD_VALUE


# 数据库中所有列都允许为空, 需要修改


class Bundle(models.Model):
    id_user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_User', blank=True, null=True,
                                verbose_name='用户名')  # Field name made lowercase.
    config_info = models.TextField(blank=True, null=True, verbose_name='AR模型的配置信息')
    product_link = models.TextField(blank=True, null=True, verbose_name='商品链接')
    QRCode = models.ImageField(blank=True, null=True, verbose_name='二维码', upload_to='QRCodes',
                               default='QRCodes/qrcode.png')
    model = models.FileField(blank=True, null=True, verbose_name='模型文件', upload_to='bundles')
    imageTarget = models.ImageField(blank=True, null=True, verbose_name='AR显示目标图片', upload_to='imageTargets')
    name = models.TextField(blank=True, null=True, verbose_name='名字')
    likes = models.IntegerField(blank=True, null=True, verbose_name='点赞数量', default=0)
    scan_times = models.IntegerField(blank=True, null=True, verbose_name='扫描次数', default=0, )
    comments = models.IntegerField(blank=True, null=True, verbose_name='评论数', default=0)
    upload_datetime = models.DateTimeField(blank=True, null=True, verbose_name='上传时间', auto_now_add=True)
    last_edit_datetime = models.DateTimeField(blank=True, null=True, verbose_name='最后一次编辑时间', auto_now=True)
    note = models.TextField(blank=True, null=True, verbose_name='描述')
    feedback_rate = models.FloatField(blank=True, null=True, verbose_name='好评率', default=0.0)
    concerned_rate = models.FloatField(blank=True, null=True, verbose_name='专注度', default=0.0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'AR模型'
        verbose_name_plural = verbose_name
        db_table = 'bundle'


class CommentStatistics(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True, null=True,
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
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_location = models.ForeignKey('Locations', models.DO_NOTHING, db_column='id_Location', blank=True,
                                    null=True, verbose_name='地区')  # Field name made lowercase.
    content = models.TextField(blank=True, null=True, verbose_name='内容')
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='时间', auto_now_add=True)
    sentiment = models.FloatField(blank=True, null=True, verbose_name='情感值')

    def comment_save_operation(self):
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
        comments = self.id_bundle.comment_set.all()
        positive = 0
        feedback_rate = 0.0
        for each_comment in comments:
            if each_comment.sentiment >= 0.55:
                positive += 1
        if self.id_bundle.comments != 0:
            feedback_rate = float(positive) / float(self.id_bundle.comments)
        else:
            pass
        self.id_bundle.feedback_rate = float('%0.2f' % feedback_rate)
        self.id_bundle.save()

    def save(self, *args, **kwargs):
        content = SnowNLP(self.content)
        self.sentiment = content.sentiments
        super(self.__class__, self).save(*args, **kwargs)
        comment_save_operation_thread = threading.Thread(target=self.comment_save_operation())
        comment_save_operation_thread.start()

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        db_table = 'comment'


class KeywordsStatistics(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True, null=True,
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
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True, null=True,
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
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    datetime = models.DateField(blank=True, null=True, verbose_name='时间')
    amount = models.IntegerField(blank=True, null=True, verbose_name='数量', default=1)

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '扫描数量统计'
        verbose_name_plural = verbose_name
        db_table = 'scan_statistics'


class Scan(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True, null=True,
                                  verbose_name='AR模型')  # Field name made lowercase.
    id_location = models.ForeignKey('Locations', models.DO_NOTHING, db_column='id_Location', blank=True,
                                    null=True, verbose_name='地区')  # Field name made lowercase.
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='时间', auto_now_add=True)

    def scan_save_operation(self):
        ScanOperatingRecord.objects.create(id_scan=self, id_bundle=self.id_bundle)
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

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        scan_save_operation_thread = threading.Thread(target=self.scan_save_operation())
        scan_save_operation_thread.start()

    def __unicode__(self):
        return self.id_bundle.name

    class Meta:
        verbose_name = '扫描记录'
        verbose_name_plural = verbose_name
        db_table = 'scan'


class ScanOperatingRecord(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True,
                                  null=True)  # Field name made lowercase.
    id_scan = models.ForeignKey(Scan, models.CASCADE, db_column='id_Scan', blank=True, null=True,
                                verbose_name='扫描记录')  # Field name made lowercase.
    commented = models.FloatField(blank=True, null=True, verbose_name='已评论', default=0)
    liked = models.IntegerField(blank=True, null=True, verbose_name='已点赞', default=0)
    product_link_clicked = models.IntegerField(blank=True, null=True, verbose_name='已点击商品链接', default=0)

    def count_concerned_rate(self):
        scan_scores = self.id_bundle.scan_set.count() * CONCERNED_THRESHOLD_VALUE['SCAN']
        comment_scores = 0.0
        like_scores = 0.0
        product_link_clicked_scores = 0.0
        for each in self.id_bundle.scanoperatingrecord_set.all():
            if each.commented > 0:
                comment_scores += each.commented
            if each.liked > 0:
                like_scores += each.liked
            if each.product_link_clicked > 0:
                product_link_clicked_scores += each.product_link_clicked
        comment_scores = comment_scores * CONCERNED_THRESHOLD_VALUE['COMMENT']
        like_scores = like_scores * CONCERNED_THRESHOLD_VALUE['LIKE']
        product_link_clicked_scores = product_link_clicked_scores * CONCERNED_THRESHOLD_VALUE['PRODUCT_LINK_CLICKED']
        concerned_rate = scan_scores + comment_scores + like_scores + product_link_clicked_scores
        self.id_bundle.concerned_rate = float('%0.2f' % concerned_rate)
        self.id_bundle.save()

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        count_concerned_rate_thread = threading.Thread(target=self.count_concerned_rate())
        count_concerned_rate_thread.start()

    def __unicode__(self):
        return self.id_scan.id_bundle.name

    class Meta:
        verbose_name = '扫描后操作记录'
        verbose_name_plural = verbose_name
        db_table = 'scan_operating_Record'


class ScanLocation(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.CASCADE, db_column='id_Bundle', blank=True, null=True,
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
