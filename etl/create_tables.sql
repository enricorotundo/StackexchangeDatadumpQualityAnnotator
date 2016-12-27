create table Badges (
  Id INT NOT NULL PRIMARY KEY,
  UserId INT,
  Name VARCHAR(50),
  Date DATETIME,
  Class SMALLINT,
  TagBased BIT(64)
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

CREATE TABLE PostHistory (
    Id INT NOT NULL PRIMARY KEY,
    PostHistoryTypeId SMALLINT NOT NULL,
    PostId INT NOT NULL,
    RevisionGUID VARCHAR(36) NOT NULL,
    CreationDate DATETIME NOT NULL,
    UserId INT,
    UserDisplayName VARCHAR(40),
    Comment VARCHAR(400),
    Text TEXT
);

CREATE TABLE PostLinks (
  Id INT NOT NULL PRIMARY KEY,
  CreationDate DATETIME DEFAULT NULL,
  PostId INT NOT NULL,
  RelatedPostId INT NOT NULL,
  LinkTypeId SMALLINT NOT NULL
);


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
    AnnotatedQuality TINYINT
);

CREATE TABLE Tags (
  Id INT NOT NULL PRIMARY KEY,
  TagName VARCHAR(50) CHARACTER SET latin1 DEFAULT NULL,
  Count INT DEFAULT NULL,
  ExcerptPostId INT DEFAULT NULL,
  WikiPostId INT DEFAULT NULL
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