# Poverty prediction from satellite imagery for Nigeria

Based on the paper “Combining satellite imagery and machine learning to predict poverty” paper by Jean, Burke, et al. (2016). 

https://www.science.org/doi/10.1126/science.aaf7894
https://github.com/nealjean/predicting-poverty

Code based on:

https://github.com/jmather625/predicting-poverty-replication


Reproduce:
- process_survey_data
- attach_light_intensities


# Installation

use different python version:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install python3.8-distutils
sudo apt-get install python3.8
```

gdal:

```
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
ogrinfo --version
```
this printed: ~GDAL 3.4.3, released 2022/04/22~

```
pip install --no-cache-dir GDAL==3.4.3
```

Hack for `collections`: change import to avoid `ImportError`:
```
ImportError: cannot import name 'Sequence' from 'collections'
```
I changed this line in some of the packages (geoio?) that I installed:
```
from collections.abc import Sequence
```
