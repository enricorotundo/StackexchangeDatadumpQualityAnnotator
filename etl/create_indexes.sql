create index Badges_idx_1 on Badges(UserId);

create index Comments_idx_1 on Comments(PostId);
create index Comments_idx_2 on Comments(UserId);

create index Post_history_idx_1 on PostHistory(PostId);
create index Post_history_idx_2 on PostHistory(UserId);

create index Posts_idx_1 on Posts(AcceptedAnswerId);
create index Posts_idx_2 on Posts(ParentId);
create index Posts_idx_3 on Posts(OwnerUserId);
create index Posts_idx_4 on Posts(LastEditorUserId);

create index Votes_idx_1 on Votes(PostId);
