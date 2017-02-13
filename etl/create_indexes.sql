
use cooking_stackexchange_com;
create index Posts_idx_1 on Posts(PostTypeId);
create index Posts_idx_2 on Posts(ParentId);

use travel_stackexchange_com;
create index Posts_idx_1 on Posts(PostTypeId);
create index Posts_idx_2 on Posts(ParentId);

use webapps_stackexchange_com;
create index Posts_idx_1 on Posts(PostTypeId);
create index Posts_idx_2 on Posts(ParentId);