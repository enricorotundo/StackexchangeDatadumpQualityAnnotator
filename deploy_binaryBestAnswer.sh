#!/usr/bin/env bash

N_PARTITIONS=16
DB='travel'
TASK_NAME='binaryBestAnswer'
SRC_FILE_NAME='threads_acceptedOnly_ansCountGte2.json'

### activate local virtualenv
source venv/bin/activate &&

### ETL from DB to local JSON files
#python manage.py ETL_stack_threads &&
#python manage.py ETL_stack_cooccurrence_network &&
#python manage.py ETL_stack_ARN_network &&
#python manage.py ETL_stack_ABAN_network &&
#python manage.py ETL_stack_CBEN_network &&
#python manage.py ETL_stack_users &&

### Merge networks data
# python -m Analysis.network_analysis

### Run the thing
python -m Analysis.feats_extract --n_partitions ${N_PARTITIONS} --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.split --n_partitions ${N_PARTITIONS} --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.preprocess --scaler robust --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME}
#python -m Analysis.train --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME}
#python -m Analysis.test --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME}
