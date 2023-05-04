# Copyright (c) 2023.
# -*-coding:utf-8 -*-
"""
@file: DataReaderCsv.py
@author: Jerry(Ruihuang)Yang
@email: rxy216@case.edu
@time: 5/3/23 23:40
"""
import csv
import numpy as np


class DataReaderCsv:
    """
    read data from csv file for cytof data
    todo: support more data tag layers, current only support 2 layers
    """
    HEADER_ROW_NUM = 2  # the number of header rows
    GROUP_TAG_ROW = 1  # the row number of group tag, first row is 0
    ROW_TAG_NUM = 2  # the number of columns of row tags

    def __init__(self, file_path):
        self.file_path = file_path
        self.group_tag_dict = {}  # group tag dictionary, key: value = group name: [start, end] index (absolute index)
        self.data_tag_dict = {}  # data tag dictionary, {layer1-1: [layer2-1, layer2-2, ...], layer1-2: [...], ...}
        self.all_data = {}  # all data
        self.read_data()

    def read_data(self):
        # read csv line by line
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            # deal with header rows
            for header_row in range(self.HEADER_ROW_NUM):
                header = next(reader)[self.ROW_TAG_NUM:]
                #  if need to do something with individual subject, do it here
                #  get group tag
                if header_row == self.GROUP_TAG_ROW:
                    self.get_group_range(header)
            #  iterate through each row
            for row in reader:
                #  get data tag
                data_tag = self.get_data_tag(row[:self.ROW_TAG_NUM])
                for group_tag in self.group_tag_dict:
                    #  store data in all_data as a numpy array
                    self.all_data[group_tag + '|' + data_tag] = np.array(row[self.group_tag_dict[group_tag][0]:
                                                                             self.group_tag_dict[group_tag][1]],
                                                                         dtype=np.float64)
            print(len(list(self.all_data.items())))

    def get_data(self, data_tag_list):
        """
        get data from all_data
        :param data_tag_list: a list of all data tags, including group tag. e.g. ['group1', 'data1', 'data2']
        if you want all data in a group or a data_tag, use 'all' instead of the specific tag
        :return: the numpy array of the selected data
        """
        list_of_data_to_get = []
        list_of_individual_tag = []
        for index, tag in enumerate(data_tag_list):
            if tag.lower() == 'all':
                list_of_individual_tag.append([])
                if index == 0:
                    for group_tag in self.group_tag_dict:
                        list_of_individual_tag[index].append(group_tag)
                elif index == 1:
                    for data_tag in self.data_tag_dict:
                        list_of_individual_tag[index].append(data_tag)
                elif index == 2:
                    temp_dict = {}
                    for data_tag in self.data_tag_dict:
                        for sub_tag in self.data_tag_dict[data_tag]:
                            temp_dict[sub_tag] = 1
                    list_of_individual_tag[index] = list(temp_dict.keys())
            else:
                list_of_individual_tag.append([tag])
        for group_tag_get in list_of_individual_tag[0]:
            for data_tag_get in list_of_individual_tag[1]:
                for sub_tag_get in list_of_individual_tag[2]:
                    list_of_data_to_get.append(group_tag_get + '|' + data_tag_get + '|' + sub_tag_get)
        data_to_return = {}
        for data_tag in list_of_data_to_get:
            if data_tag in self.all_data:
                data_to_return[data_tag] = self.all_data[data_tag]
        return data_to_return

    def get_group_range(self, group_header):
        """
        get the range of each group
        todo: get rid of the blank space in the group name
        :param group_header: the header row of group tag
        :return:
        """
        last_cut_index = 0
        for i in range(1, len(group_header)):
            if group_header[i] != group_header[i - 1]:
                self.group_tag_dict[group_header[i - 1]] = [last_cut_index + self.ROW_TAG_NUM, i + self.ROW_TAG_NUM]
                last_cut_index = i
        self.group_tag_dict[group_header[last_cut_index]] = [last_cut_index + self.ROW_TAG_NUM,
                                                             len(group_header) + self.ROW_TAG_NUM]

    def get_data_tag(self, tags):
        data_tag_list = []
        for tag in tags:
            data_tag_list.append(tag.replace(' ', ''))  # remove space
        data_tag = '|'.join(data_tag_list)
        if data_tag_list[0] not in self.data_tag_dict:
            self.data_tag_dict[data_tag_list[0]] = [data_tag_list[1]]
        else:
            self.data_tag_dict[data_tag_list[0]].append(data_tag_list[1])
        return data_tag


if __name__ == '__main__':
    drs = DataReaderCsv('MiceCYTOF.csv')
    print(drs.get_data(['all', 'BCell', 'pERK']))
    print(len(drs.get_data(['all', 'all', 'all'])))
