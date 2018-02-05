#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from datetime import *
from time import strftime, localtime, sleep

from tushare_api_rsi import TushareApiRsi

if __name__ == '__main__':
    """
    tushare_download data downloader to prepare the local data environment.
    """

    TushareApiRsi().calculate_rsi()