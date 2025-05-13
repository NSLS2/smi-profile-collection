#!/bin/bash

cp -v smi_config.csv ~/.ipython/profile_${TEST_PROFILE}/smi_config.csv

conda env list
python3 -m pip install --upgrade ophyd