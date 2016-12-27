from __future__ import unicode_literals

from django.db import models


class Badge(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    class_field = models.SmallIntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    tagbased = models.TextField(db_column='TagBased', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Badges'


class Comment(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    postid = models.IntegerField(db_column='PostId')  # Field name made lowercase.
    score = models.IntegerField(db_column='Score')  # Field name made lowercase.
    text = models.TextField(db_column='Text', blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate', blank=True, null=True)  # Field name made lowercase.
    userdisplayname = models.CharField(db_column='UserDisplayName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comments'


class PostHistory(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    posthistorytypeid = models.SmallIntegerField(db_column='PostHistoryTypeId')  # Field name made lowercase.
    postid = models.IntegerField(db_column='PostId')  # Field name made lowercase.
    revisionguid = models.CharField(db_column='RevisionGUID', max_length=36)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    userdisplayname = models.CharField(db_column='UserDisplayName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=400, blank=True, null=True)  # Field name made lowercase.
    text = models.TextField(db_column='Text', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PostHistory'


class PostLink(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate', blank=True, null=True)  # Field name made lowercase.
    postid = models.IntegerField(db_column='PostId')  # Field name made lowercase.
    relatedpostid = models.IntegerField(db_column='RelatedPostId')  # Field name made lowercase.
    linktypeid = models.SmallIntegerField(db_column='LinkTypeId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PostLinks'


class Post(models.Model):
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
    annotatedquality = models.IntegerField(db_column='AnnotatedQuality', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Posts'


class Tag(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    tagname = models.CharField(db_column='TagName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    excerptpostid = models.IntegerField(db_column='ExcerptPostId', blank=True, null=True)  # Field name made lowercase.
    wikipostid = models.IntegerField(db_column='WikiPostId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tags'


class User(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    reputation = models.IntegerField(db_column='Reputation')  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate', blank=True, null=True)  # Field name made lowercase.
    displayname = models.CharField(db_column='DisplayName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    lastaccessdate = models.DateTimeField(db_column='LastAccessDate')  # Field name made lowercase.
    websiteurl = models.CharField(db_column='WebsiteUrl', max_length=256, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=256, blank=True, null=True)  # Field name made lowercase.
    aboutme = models.TextField(db_column='AboutMe', blank=True, null=True)  # Field name made lowercase.
    views = models.IntegerField(db_column='Views', blank=True, null=True)  # Field name made lowercase.
    upvotes = models.IntegerField(db_column='UpVotes', blank=True, null=True)  # Field name made lowercase.
    downvotes = models.IntegerField(db_column='DownVotes', blank=True, null=True)  # Field name made lowercase.
    profileimageurl = models.CharField(db_column='ProfileImageUrl', max_length=200, blank=True, null=True)  # Field name made lowercase.
    emailhash = models.CharField(db_column='EmailHash', max_length=32, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'


class Vote(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    postid = models.IntegerField(db_column='PostId')  # Field name made lowercase.
    votetypeid = models.SmallIntegerField(db_column='VoteTypeId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate', blank=True, null=True)  # Field name made lowercase.
    bountyamount = models.IntegerField(db_column='BountyAmount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Votes'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'