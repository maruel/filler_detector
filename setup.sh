#!/bin/bash

set -eu

# sudo apt install gcc python3-virtualenv

echo "Checking for nvidia hardware"
lspci | grep -i nvidia


virtualenv --quiet .
source bin/activate
# From:
#   pip install tensorflow
#   pip freeze > requirements.txt
pip install -r requirements.txt


# Cuda:
# Visit
# https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=2004

# wget https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux.run
# mkdir drv
# sh cuda_11.1.0_455.23.05_linux.run --extract=drv
# sudo sh cuda_11.1.0_455.23.05_linux.run

# https://www.tensorflow.org/install/gpu#software_requirements
# https://developer.nvidia.com/rdp/cudnn-download
# https://developer.nvidia.com/rdp/cudnn-archive
# select 7.6.5 for Linux
# tar xvf ...
# sudo mv cuda/ /usr/local/cudnn
# sudo ldconfig /usr/local/cuda/lib64
# sudo ldconfig /usr/local/cudnn/lib64
