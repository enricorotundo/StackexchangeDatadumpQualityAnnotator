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

python -m Analysis.feats_extract_binaryBestAnswer --n_partitions ${N_PARTITIONS} --draft &&
python -m Analysis.split_binaryBestAnswer --n_partitions ${N_PARTITIONS} --draft &&
python -m Analysis.preprocess_binaryBestAnswer --draft &&
python -m Analysis.train_binaryBestAnswer --draft