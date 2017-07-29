#!/usr/bin/env bash

N_PARTITIONS=4 # to resemble a real deployment should be > 1
DB='travel'
TASK_NAME='binaryBestAnswer'
SRC_FILE_NAME='threads_acceptedOnly_all.json'

### activate local virtualenv
source venv/bin/activate &&

### ETL from DB to local JSON files
python manage.py ETL_stack_threads &&
python manage.py ETL_stack_cooccurrence_network &&
python manage.py ETL_stack_ARN_network &&
python manage.py ETL_stack_ABAN_network &&
python manage.py ETL_stack_CBEN_network &&
python manage.py ETL_stack_users &&

### Merge networks data
python -m Analysis.network_analysis

### Run
python -m Analysis.feats_extract --draft --n_partitions ${N_PARTITIONS} --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.split --draft --n_partitions ${N_PARTITIONS} --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.preprocess --draft --scaler robust --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.train --draft --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME}
python -m Analysis.test --draft --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME}
