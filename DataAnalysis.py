# Copyright (c) 2023.
# -*-coding:utf-8 -*-
"""
@file: DataAnalysis.py
@author: Jerry(Ruihuang)Yang
@email: rxy216@case.edu
@time: 5/4/23 20:56
"""
from DataReaderCsv import DataReaderCsv


class DataAnalysis:
    """
    do data analysis
    """
    FILE_PATH = 'MiceCYTOF.csv'

    def __init__(self):
        self.data_reader = DataReaderCsv(self.FILE_PATH)

    def three_d_group_analysis(self):
        pass


