# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Posts(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    posttypeid = models.IntegerField(db_column='PostTypeId')  # Field name made lowercase.
    acceptedanswerid = models.IntegerField(db_column='AcceptedAnswerId', blank=True, null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    deletiondate = models.DateTimeField(db_column='DeletionDate', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    owneruserid = models.IntegerField(db_column='OwnerUserId', blank=True, null=True)  # Field name made lowercase.
    ownerdisplayname = models.CharField(db_column='OwnerDisplayName', max_length=256, blank=True, null=True)  # Field name made lowercase.
    lasteditoruserid = models.IntegerField(db_column='LastEditorUserId', blank=True, null=True)  # Field name made lowercase.
    lasteditordisplayname = models.CharField(db_column='LastEditorDisplayName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    lasteditdate = models.DateTimeField(db_column='LastEditDate', blank=True, null=True)  # Field name made lowercase.
    lastactivitydate = models.DateTimeField(db_column='LastActivityDate', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=256, blank=True, null=True)  # Field name made lowercase.
    tags = models.CharField(db_column='Tags', max_length=256, blank=True, null=True)  # Field name made lowercase.
    answercount = models.IntegerField(db_column='AnswerCount', blank=True, null=True)  # Field name made lowercase.
    commentcount = models.IntegerField(db_column='CommentCount', blank=True, null=True)  # Field name made lowercase.
    favoritecount = models.IntegerField(db_column='FavoriteCount', blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    communityowneddate = models.DateTimeField(db_column='CommunityOwnedDate', blank=True, null=True)  # Field name made lowercase.
    annotatedqualityenrico = models.IntegerField(db_column='AnnotatedQualityEnrico', blank=True, null=True)  # Field name made lowercase.
    annotatedqualitymarit = models.IntegerField(db_column='AnnotatedQualityMarit', blank=True, null=True)  # Field name made lowercase.
    annotatedqualitychristine = models.IntegerField(db_column='AnnotatedQualityChristine', blank=True, null=True)  # Field name made lowercase.
    annotatedqualityhenrik = models.IntegerField(db_column='AnnotatedQualityHenrik', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Posts'
