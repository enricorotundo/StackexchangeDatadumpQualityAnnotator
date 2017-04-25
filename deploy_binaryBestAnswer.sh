#!/usr/bin/env bash

source venv/bin/activate &&
python -m Analysis.feats_extract_binaryBestAnswer &&
python -m Analysis.preprocess_binaryBestAnswer &&
python -m Analysis.split_binaryBestAnswer &&
python -m Analysis.train_binaryBestAnswer
