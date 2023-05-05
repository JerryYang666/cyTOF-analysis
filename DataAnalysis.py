# Copyright (c) 2023.
# -*-coding:utf-8 -*-
"""
@file: DataAnalysis.py
@author: Jerry(Ruihuang)Yang
@email: rxy216@case.edu
@time: 5/4/23 20:56
"""
import numpy as np

from DataReaderCsv import DataReaderCsv


class DataAnalysis:
    """
    do data analysis
    """
    FILE_PATH = 'MiceCYTOF.csv'

    def __init__(self):
        self.all_columns = {}
        self.data_reader = DataReaderCsv(self.FILE_PATH)
        self.all_data_tags = [self.data_reader.group_list, self.data_reader.data_tag1_list,
                              self.data_reader.data_tag2_list]

    def generate_all_columns(self):
        """
        do 3d group analysis
        :return: None
        """
        combinations = [[0, 1], [0, 2], [1, 2]]
        for combination in combinations:
            for i in self.all_data_tags[combination[0]]:
                for j in self.all_data_tags[combination[1]]:
                    column_tag_list = ['all', 'all', 'all']
                    column_tag_list[combination[0]] = i
                    column_tag_list[combination[1]] = j
                    self.all_columns['|'.join(column_tag_list)] = self.one_column_analysis(column_tag_list)

    def one_column_analysis(self, data_tags):
        """
        do one column analysis
        :param data_tags: a list of data tags, with the focused variable as 'all' e.g. ['all', 'BCell', 'pERK']
        :return: a dict of analysis results e.g. {all|BCell|pERK: {group1: {seq: 0, mean: 10.1}, group2: {...}, ...}, ...}
        """
        #  get data
        data = self.data_reader.get_data(data_tags)
        #  do sort
        mean_dict = {}
        for point in data:
            mean_dict[point] = np.mean(data[point])
        sorted_mean_dict = sorted(mean_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        sorted_dict = {}
        for i, point in enumerate(sorted_mean_dict):
            sorted_dict[point[0]] = {'seq': i, 'mean': point[1]}
        return sorted_dict


if __name__ == '__main__':
    data_analysis = DataAnalysis()
    data_analysis.generate_all_columns()
    print(len(data_analysis.all_columns))
