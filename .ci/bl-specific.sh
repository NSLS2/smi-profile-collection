#!/bin/bash

mkdir -p -v ~/.ipython/profile_test
cp -v smi_config.csv ~/.ipython/profile_test/smi_config.csv

conda activate $HOME/env
conda env list
python3 -m pip install --upgrade ophyd
conda list