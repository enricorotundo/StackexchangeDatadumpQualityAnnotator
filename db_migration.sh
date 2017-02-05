#!/bin/bash

echo "cooking_stackexchange_com"
sudo mysqldump -u root \
    --databases cooking_stackexchange_com \
    --single-transaction \
    --compress \
    --order-by-primary  \
    -proot | mysql -u awsuser \
        --port=3306 \
        --host=mydbinstance.crxqv1d0b0kd.eu-west-1.rds.amazonaws.com \
        -poPs-3la-vh6-0dv
echo "DONE!"


echo "travel_stackexchange_com"
sudo mysqldump -u root \
    --databases travel_stackexchange_com \
    --single-transaction \
    --compress \
    --order-by-primary  \
    -proot | mysql -u awsuser \
        --port=3306 \
        --host=mydbinstance.crxqv1d0b0kd.eu-west-1.rds.amazonaws.com \
        -poPs-3la-vh6-0dv
echo "DONE!"


echo "webapps_stackexchange_com"
sudo mysqldump -u root \
    --databases webapps_stackexchange_com \
    --single-transaction \
    --compress \
    --order-by-primary  \
    -proot | mysql -u awsuser \
        --port=3306 \
        --host=mydbinstance.crxqv1d0b0kd.eu-west-1.rds.amazonaws.com \
        -poPs-3la-vh6-0dv
echo "DONE!"
