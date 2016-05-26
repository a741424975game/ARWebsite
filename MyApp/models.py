from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Bundle(models.Model):
    id_user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_User', blank=True, null=True)  # Field name made lowercase.
    url = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    like = models.IntegerField(blank=True, null=True)
    scan_times = models.IntegerField(blank=True, null=True)
    datetime = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bundle'

class Comment(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True)  # Field name made lowercase.
    id_comment_location = models.ForeignKey('CommentLocation', models.DO_NOTHING, db_column='id_Comment_Location', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)
    datetime = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.content

    class Meta:
        db_table = 'comment'

class CommentLocation(models.Model):
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.location

    class Meta:
        db_table = 'comment_location'

class Scan(models.Model):
    id_bundle = models.ForeignKey(Bundle, models.DO_NOTHING, db_column='id_Bundle', blank=True, null=True)  # Field name made lowercase.
    id_scan_location = models.ForeignKey('ScanLocation', models.DO_NOTHING, db_column='id_Scan_Location', blank=True, null=True)  # Field name made lowercase.

    def __unicode__(self):
        return self.id_bundle

    class Meta:
        db_table = 'scan'

class ScanLocation(models.Model):
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.location

    class Meta:
        db_table = 'scan_location'

