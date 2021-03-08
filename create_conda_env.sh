#!/bin/bash
conda create --override-channels -y \
    -c conda-forge -c anaconda \
    -n exac_va \
    python==3.7.1 \
    pytest \
    numpy \
    aiohttp \
    pytest-aiohttp
