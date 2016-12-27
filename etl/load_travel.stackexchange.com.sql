load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Badges.xml'
into table Badges
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Comments.xml'
into table Comments
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/PostHistory.xml'
into table PostHistory
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/PostLinks.xml'
INTO TABLE PostLinks
ROWS IDENTIFIED BY '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Posts.xml'
into table Posts
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Tags.xml'
INTO TABLE Tags
ROWS IDENTIFIED BY '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Users.xml'
into table Users
rows identified by '<row>';

load xml infile '/Users/erotundo/PycharmProjects/DatasetAnnotator/data_source/stackexchange_v12Sept2016/travel.stackexchange.com/Votes.xml'
into table Votes
rows identified by '<row>';
