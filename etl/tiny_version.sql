create database cooking_stackexchange_com DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
create database travel_stackexchange_com DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
create database webapps_stackexchange_com DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

###############
USE cooking_stackexchange_com;

CREATE TABLE Posts (
    Id INT NOT NULL PRIMARY KEY,
    PostTypeId TINYINT NOT NULL ,
    AcceptedAnswerId INT,
    ParentId INT,
    CreationDate DATETIME NOT NULL,
    DeletionDate DATETIME,
    Score INT NULL,
    ViewCount INT NULL,
    Body text NULL,
    OwnerUserId INT,
    OwnerDisplayName varchar(256),
    LastEditorUserId INT,
    LastEditorDisplayName VARCHAR(40),
    LastEditDate DATETIME,
    LastActivityDate DATETIME,
    Title varchar(256),
    Tags VARCHAR(256),
    AnswerCount INT DEFAULT 0,
    CommentCount INT DEFAULT 0,
    FavoriteCount INT DEFAULT 0,
    ClosedDate DATETIME,
    CommunityOwnedDate DATETIME,
    AnnotatedQualityEnrico TINYINT,
    AnnotatedQualityMarit TINYINT,
    AnnotatedQualityChristine TINYINT,
    AnnotatedQualityHenrik TINYINT
);


load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/data_source/stackexchange_v12Sept2016/cooking.stackexchange.com/Posts.xml'
into table Posts
rows identified by '<row>';


###############
USE travel_stackexchange_com;

CREATE TABLE Posts (
    Id INT NOT NULL PRIMARY KEY,
    PostTypeId TINYINT NOT NULL ,
    AcceptedAnswerId INT,
    ParentId INT,
    CreationDate DATETIME NOT NULL,
    DeletionDate DATETIME,
    Score INT NULL,
    ViewCount INT NULL,
    Body text NULL,
    OwnerUserId INT,
    OwnerDisplayName varchar(256),
    LastEditorUserId INT,
    LastEditorDisplayName VARCHAR(40),
    LastEditDate DATETIME,
    LastActivityDate DATETIME,
    Title varchar(256),
    Tags VARCHAR(256),
    AnswerCount INT DEFAULT 0,
    CommentCount INT DEFAULT 0,
    FavoriteCount INT DEFAULT 0,
    ClosedDate DATETIME,
    CommunityOwnedDate DATETIME,
    AnnotatedQualityEnrico TINYINT,
    AnnotatedQualityMarit TINYINT,
    AnnotatedQualityChristine TINYINT,
    AnnotatedQualityHenrik TINYINT
);


load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Posts.xml'
into table Posts
rows identified by '<row>';

########################
USE webapps_stackexchange_com;

CREATE TABLE Posts (
    Id INT NOT NULL PRIMARY KEY,
    PostTypeId TINYINT NOT NULL ,
    AcceptedAnswerId INT,
    ParentId INT,
    CreationDate DATETIME NOT NULL,
    DeletionDate DATETIME,
    Score INT NULL,
    ViewCount INT NULL,
    Body text NULL,
    OwnerUserId INT,
    OwnerDisplayName varchar(256),
    LastEditorUserId INT,
    LastEditorDisplayName VARCHAR(40),
    LastEditDate DATETIME,
    LastActivityDate DATETIME,
    Title varchar(256),
    Tags VARCHAR(256),
    AnswerCount INT DEFAULT 0,
    CommentCount INT DEFAULT 0,
    FavoriteCount INT DEFAULT 0,
    ClosedDate DATETIME,
    CommunityOwnedDate DATETIME,
    AnnotatedQualityEnrico TINYINT,
    AnnotatedQualityMarit TINYINT,
    AnnotatedQualityChristine TINYINT,
    AnnotatedQualityHenrik TINYINT
);

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/data_source/stackexchange_v12Sept2016/webapps.stackexchange.com/Posts.xml'
into table Posts
rows identified by '<row>';