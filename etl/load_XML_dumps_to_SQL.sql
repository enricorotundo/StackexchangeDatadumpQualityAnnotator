# first run this in the localhost MySQL, then run db_upload.sh to move it online

create database cooking_stackexchange_com DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

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

CREATE TABLE Users (
    Id INT NOT NULL PRIMARY KEY,
    Reputation INT NOT NULL,
    CreationDate DATETIME,
    DisplayName VARCHAR(40) NULL,
    LastAccessDate  DATETIME NOT NULL,
    WebsiteUrl VARCHAR(256) NULL,
    Location VARCHAR(256) NULL,
    AboutMe TEXT NULL,
    Views INT DEFAULT 0,
    UpVotes INT,
    DownVotes INT,
    ProfileImageUrl VARCHAR(200) NULL,
    EmailHash VARCHAR(32),
    Age INT NULL,
    AccountId INT NULL
);

CREATE TABLE Votes (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    VoteTypeId SMALLINT NOT NULL,
    UserId INT,
    CreationDate DATETIME,
    BountyAmount INT
);

CREATE TABLE Comments (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    Score INT NOT NULL DEFAULT 0,
    Text TEXT,
    CreationDate DATETIME,
    UserDisplayName VARCHAR(30),
    UserId INT
);

create table Badges (
  Id INT NOT NULL PRIMARY KEY,
  UserId INT,
  Name VARCHAR(50),
  Date DATETIME,
  Class SMALLINT,
  TagBased BIT(64)
);

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/cooking.stackexchange.com/Posts.xml'
into table Posts
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/cooking.stackexchange.com/Users.xml'
into table Users
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/cooking.stackexchange.com/Votes.xml'
into table Votes
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/cooking.stackexchange.com/Comments.xml'
into table Comments
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/cooking.stackexchange.com/Badges.xml'
into table Badges
rows identified by '<row>';

###############

create database travel_stackexchange_com DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

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

CREATE TABLE Users (
    Id INT NOT NULL PRIMARY KEY,
    Reputation INT NOT NULL,
    CreationDate DATETIME,
    DisplayName VARCHAR(40) NULL,
    LastAccessDate  DATETIME NOT NULL,
    WebsiteUrl VARCHAR(256) NULL,
    Location VARCHAR(256) NULL,
    AboutMe TEXT NULL,
    Views INT DEFAULT 0,
    UpVotes INT,
    DownVotes INT,
    ProfileImageUrl VARCHAR(200) NULL,
    EmailHash VARCHAR(32),
    Age INT NULL,
    AccountId INT NULL
);

CREATE TABLE Votes (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    VoteTypeId SMALLINT NOT NULL,
    UserId INT,
    CreationDate DATETIME,
    BountyAmount INT
);

CREATE TABLE Comments (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    Score INT NOT NULL DEFAULT 0,
    Text TEXT,
    CreationDate DATETIME,
    UserDisplayName VARCHAR(30),
    UserId INT
);

create table Badges (
  Id INT NOT NULL PRIMARY KEY,
  UserId INT,
  Name VARCHAR(50),
  Date DATETIME,
  Class SMALLINT,
  TagBased BIT(64)
);

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Posts.xml'
into table Posts
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Users.xml'
into table Users
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Votes.xml'
into table Votes
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Comments.xml'
into table Comments
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Badges.xml'
into table Badges
rows identified by '<row>';

########################
create database webapps_stackexchange_com DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

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

CREATE TABLE Users (
    Id INT NOT NULL PRIMARY KEY,
    Reputation INT NOT NULL,
    CreationDate DATETIME,
    DisplayName VARCHAR(40) NULL,
    LastAccessDate  DATETIME NOT NULL,
    WebsiteUrl VARCHAR(256) NULL,
    Location VARCHAR(256) NULL,
    AboutMe TEXT NULL,
    Views INT DEFAULT 0,
    UpVotes INT,
    DownVotes INT,
    ProfileImageUrl VARCHAR(200) NULL,
    EmailHash VARCHAR(32),
    Age INT NULL,
    AccountId INT NULL
);

CREATE TABLE Votes (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    VoteTypeId SMALLINT NOT NULL,
    UserId INT,
    CreationDate DATETIME,
    BountyAmount INT
);

CREATE TABLE Comments (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    Score INT NOT NULL DEFAULT 0,
    Text TEXT,
    CreationDate DATETIME,
    UserDisplayName VARCHAR(30),
    UserId INT
);

create table Badges (
  Id INT NOT NULL PRIMARY KEY,
  UserId INT,
  Name VARCHAR(50),
  Date DATETIME,
  Class SMALLINT,
  TagBased BIT(64)
);

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/webapps.stackexchange.com/Posts.xml'
into table Posts
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/webapps.stackexchange.com/Users.xml'
into table Users
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/webapps.stackexchange.com/Votes.xml'
into table Votes
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/webapps.stackexchange.com/Comments.xml'
into table Comments
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotatorProj/etl/data_source/stackexchange_v12Sept2016/webapps.stackexchange.com/Badges.xml'
into table Badges
rows identified by '<row>';



##########

create database stackoverflow_com DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

USE stackoverflow_com;

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

CREATE TABLE Users (
    Id INT NOT NULL PRIMARY KEY,
    Reputation INT NOT NULL,
    CreationDate DATETIME,
    DisplayName VARCHAR(40) NULL,
    LastAccessDate  DATETIME NOT NULL,
    WebsiteUrl VARCHAR(256) NULL,
    Location VARCHAR(256) NULL,
    AboutMe TEXT NULL,
    Views INT DEFAULT 0,
    UpVotes INT,
    DownVotes INT,
    ProfileImageUrl VARCHAR(200) NULL,
    EmailHash VARCHAR(32),
    Age INT NULL,
    AccountId INT NULL
);

CREATE TABLE Votes (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    VoteTypeId SMALLINT NOT NULL,
    UserId INT,
    CreationDate DATETIME,
    BountyAmount INT
);

CREATE TABLE Comments (
    Id INT NOT NULL PRIMARY KEY,
    PostId INT NOT NULL,
    Score INT NOT NULL DEFAULT 0,
    Text TEXT,
    CreationDate DATETIME,
    UserDisplayName VARCHAR(30),
    UserId INT
);

create table Badges (
  Id INT NOT NULL PRIMARY KEY,
  UserId INT,
  Name VARCHAR(50),
  Date DATETIME,
  Class SMALLINT,
  TagBased BIT(64)
);

# TODO add the XML loading for stackoverflow