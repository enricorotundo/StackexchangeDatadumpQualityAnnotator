#!/usr/bin/env bash

# activate local virtualenv
source venv/bin/activate &&

# TODO should run the preliminary DB analysis located in Analysis/Tasks/BestAnswer
# http://stackoverflow.com/questions/35545402/running-ipynb-from-terminal

# ETL from DB to local JSON files
#python manage.py ETL_stack_threads &&
#python manage.py ETL_stack_cooccurrence_network &&
#python manage.py ETL_stack_ARN_network &&
#python manage.py ETL_stack_ABAN_network &&
#python manage.py ETL_stack_CBEN_network &&
#python manage.py ETL_stack_users &&

N_PARTITIONS=4 # to resemble real deploy should be > 1
DB='travel'
TASK_NAME='binaryBestAnswer'
SRC_FILE_NAME='threads_acceptedOnly_ansCountGte4.json'

python -m Analysis.feats_extract --draft --n_partitions ${N_PARTITIONS} --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.split --draft --n_partitions ${N_PARTITIONS} --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.preprocess --draft --scaler robust --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME} &&
python -m Analysis.train --draft --db ${DB} --task_name ${TASK_NAME} --src_file_name ${SRC_FILE_NAME}
