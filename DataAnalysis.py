# Copyright (c) 2023.
# -*-coding:utf-8 -*-
"""
@file: DataAnalysis.py
@author: Jerry(Ruihuang)Yang and Jayant Siva
@email: rxy216@case.edu
@time: 5/22/23 20:56
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns

from DataReaderCsv import DataReaderCsv


def closest_factors(n):
    for i in range(int(n ** 0.5), 0, -1):
        if n % i == 0:
            return i, n // i


class DataAnalysis:
    """
    do data analysis
    """
    FILE_PATH = 'MiceCYTOF.csv'

    def __init__(self, control_group='Naïve'):
        self.grant_data = None
        self.CONTROL_GROUP = control_group
        self.all_columns = {}
        self.data_reader = DataReaderCsv(self.FILE_PATH)
        self.all_data_tags = [self.data_reader.group_list, self.data_reader.data_tag1_list,
                              self.data_reader.data_tag2_list]
        self.all_data_tags_name = ['group', 'Cell Type', 'Marker']

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
            percent_from_control = 0
            if self.CONTROL_GROUP not in point[0]:
                control_for_point = point[0].replace(point[0].split('|')[0], self.CONTROL_GROUP)
                control_data = self.data_reader.get_data(control_for_point.split('|'))
                percent_from_control = (np.mean(mean_dict[point[0]]) - np.mean(control_data[control_for_point])) / \
                                       np.mean(control_data[control_for_point])
            sorted_dict[point[0]] = {'seq': i, 'mean': point[1], 'percent_from_control': percent_from_control}
        return sorted_dict

    def get_surface_data(self, all_data_tag_index, surface_name, plot_type):
        """
        get surface data
        :param plot_type: seq or mean
        :param all_data_tag_index: 0, 1, 2, which axis is the focused variable
        :param surface_name: what is the focused variable of the surface
        :return: surfaced data, x label, y label
        """
        surface_data = []
        xy_label = {}  # index is the axis index from all axis, value is the axis label
        temp_xy_index = []
        for index, axis in enumerate(self.all_data_tags):
            if index != all_data_tag_index:
                xy_label[index] = axis
                temp_xy_index.append(index)
        for i in xy_label[temp_xy_index[0]]:
            row = []
            for j in xy_label[temp_xy_index[1]]:
                column_tag_list = ['all', 'all', 'all']
                column_tag_list[temp_xy_index[0]] = i
                column_tag_list[temp_xy_index[1]] = j
                # print(column_tag_list)
                point_tag = []
                for t in column_tag_list:
                    if t != 'all':
                        point_tag.append(t)
                    else:
                        point_tag.append(surface_name)
                # print(point_tag)
                row.append(self.all_columns['|'.join(column_tag_list)]['|'.join(point_tag)][plot_type])
            surface_data.append(row)
        return np.array(surface_data), xy_label[temp_xy_index[1]], xy_label[temp_xy_index[0]]

    def plot_surface(self, plot_type, color_map='gist_earth_r'):
        """
        plot 2d surface
        :param plot_type: 'seq' or 'mean'
        :return: None
        """
        if plot_type == 'seq':
            color_map = 'Blues_r'
        for index, axis in enumerate(self.all_data_tags):
            #  get subplot row and col
            subplot_row, subplot_col = closest_factors(len(axis))  # type: ignore
            # Set up the plot
            fig, axs = plt.subplots(nrows=subplot_row, ncols=subplot_col,
                                    figsize=(subplot_col * 8, subplot_row * 8),
                                    gridspec_kw={'hspace': 0.1, 'wspace': 0.15})
            fig.suptitle(f'CyTOF {self.all_data_tags_name[index]} {plot_type} surface', fontsize=32)
            tick_no = 0
            for i in range(0, subplot_row):
                for j in range(0, subplot_col):
                    surface_data, x, y = self.get_surface_data(index, axis[tick_no], plot_type)
                    print(surface_data)
                    # print(x)
                    # print(y)
                    if subplot_row == 1 or subplot_col == 1:
                        p = 0
                        # if plot_type == 'percent_from_control', we need to put the center of the color bar at 0
                        if plot_type == 'percent_from_control':
                            p = axs[tick_no].imshow(surface_data, cmap=color_map, norm=colors.CenteredNorm())
                        else:
                            p = axs[tick_no].imshow(surface_data, cmap=color_map)
                        plt.colorbar(p, ax=axs[tick_no])
                        axs[tick_no].set_xticks(np.arange(len(x)), x, rotation=60)
                        axs[tick_no].set_yticks(np.arange(len(y)), y)
                        axs[tick_no].set_title(f'{axis[tick_no]},')
                    else:
                        p = 0
                        # if plot_type == 'percent_from_control', we need to put the center of the color bar at 0
                        if plot_type == 'percent_from_control':
                            p = axs[i, j].imshow(surface_data, cmap=color_map, norm=colors.CenteredNorm())
                        else:
                            p = axs[i, j].imshow(surface_data, cmap=color_map)
                        plt.colorbar(p, ax=axs[i, j])
                        axs[i, j].set_xticks(np.arange(len(x)), x, rotation=60)
                        axs[i, j].set_yticks(np.arange(len(y)), y)
                        axs[i, j].set_title(f'{axis[tick_no]},')
                    tick_no += 1
            plt.show()

    def plot_for_grant(self, plot_type, color_map='gist_earth_r'):
        """
        plot 2d surface
        :param plot_type: 'seq' or 'mean'
        :return: None
        """
        if plot_type == 'seq':
            color_map = 'Blues_r'
        for index, axis in enumerate(self.all_data_tags):
            all_surface_data = []
            x = None
            y = None
            for name in axis:
                if "IL7" not in name and "+" not in name:
                    surface_data, x, y = self.get_surface_data(index, name, plot_type)
                    all_surface_data.append(np.transpose(surface_data))

            self.grant_data = all_surface_data
            return
            all_surface_data = np.concatenate(all_surface_data, axis=1)
            print(all_surface_data)
            # set size
            plt.figure(figsize=(7, 7))
            plt.imshow(all_surface_data, cmap=color_map, norm=colors.CenteredNorm())
            plt.colorbar()
            plt.xticks(np.arange(len(y * 3)), y * 3, rotation=80)
            plt.yticks(np.arange(len(x)), x)
            # put x tick on top
            ax = plt.gca()
            ax.xaxis.tick_top()
            # plot a line to separate the groups
            plt.axvline(x=len(y) - 0.5, color='black')
            plt.axvline(x=len(y) * 2 - 0.5, color='black')
            # mark the groups on the bottom
            plt.text(len(y) / 2 - 0.5, 19, 'Heme', ha='center', va='center', fontsize=12)
            plt.text(len(y) * 1.5 - 0.5, 19, 'Sepsis', ha='center', va='center', fontsize=12)
            plt.text(len(y) * 2.5 - 0.5, 19, 'Sepsis + Heme', ha='center', va='center', fontsize=12)
            plt.show()
            return

            #  get subplot row and col
            subplot_row, subplot_col = closest_factors(len(axis))  # type: ignore
            # Set up the plot
            fig, axs = plt.subplots(nrows=subplot_row, ncols=subplot_col,
                                    figsize=(subplot_col * 8, subplot_row * 8),
                                    gridspec_kw={'hspace': 0.1, 'wspace': 0.15})
            fig.suptitle(f'CyTOF {self.all_data_tags_name[index]} {plot_type} surface', fontsize=32)

            tick_no = 0
            for i in range(0, subplot_row):
                for j in range(0, subplot_col):
                    if "IL7" in axis[tick_no]:
                        tick_no += 1
                        continue
                    surface_data, x, y = self.get_surface_data(index, axis[tick_no], plot_type)
                    print(surface_data)
                    # print(x)
                    # print(y)
                    if subplot_row == 1 or subplot_col == 1:
                        p = 0
                        # if plot_type == 'percent_from_control', we need to put the center of the color bar at 0
                        if plot_type == 'percent_from_control':
                            p = axs[tick_no].imshow(surface_data, cmap=color_map, norm=colors.CenteredNorm())
                        else:
                            p = axs[tick_no].imshow(surface_data, cmap=color_map)
                        plt.colorbar(p, ax=axs[tick_no])
                        axs[tick_no].set_xticks(np.arange(len(x)), x, rotation=60)
                        axs[tick_no].set_yticks(np.arange(len(y)), y)
                        axs[tick_no].set_title(f'{axis[tick_no]},')
                    else:
                        p = 0
                        # if plot_type == 'percent_from_control', we need to put the center of the color bar at 0
                        if plot_type == 'percent_from_control':
                            p = axs[i, j].imshow(surface_data, cmap=color_map, norm=colors.CenteredNorm())
                        else:
                            p = axs[i, j].imshow(surface_data, cmap=color_map)
                        plt.colorbar(p, ax=axs[i, j])
                        axs[i, j].set_xticks(np.arange(len(x)), x, rotation=60)
                        axs[i, j].set_yticks(np.arange(len(y)), y)
                        axs[i, j].set_title(f'{axis[tick_no]},')
                    tick_no += 1
            plt.show()
            break

    def plot_for_grant2(self, plot_type, color_map='gist_earth_r'):
        """
        plot 2d surface
        :param plot_type: 'seq' or 'mean'
        :return: None
        """
        if plot_type == 'seq':
            color_map = 'Blues_r'
        for index, axis in enumerate(self.all_data_tags):
            a_all_surface_data = []
            x = None
            y = None
            for name in axis:
                if "CLP + Heme" in name:
                    surface_data, x, y = self.get_surface_data(index, name, plot_type)
                    a_all_surface_data.append(np.transpose(surface_data))
            self.grant_data = a_all_surface_data
            return


if __name__ == '__main__':
    data_analysis = DataAnalysis("Naïve")
    data_analysis.generate_all_columns()
    # data_analysis.plot_surface('mean')
    # data_analysis.plot_surface('seq')
    # data_analysis.plot_surface('percent_from_control', color_map='RdYlGn')
    data_analysis.plot_for_grant('percent_from_control', color_map='RdYlGn')
    frist_two = data_analysis.grant_data
    da2 = DataAnalysis("CLP (HemeV)")
    da2.generate_all_columns()
    da2.plot_for_grant2('percent_from_control', color_map='RdYlGn')
    third = da2.grant_data
    _, x, y = data_analysis.get_surface_data(0, "Naïve", "percent_from_control")
    frist_two.append(third[0])
    all_surface_data = frist_two
    all_surface_data = np.concatenate(all_surface_data, axis=1)
    print(all_surface_data)
    # set size
    plt.figure(figsize=(7, 7))
    plt.imshow(all_surface_data, cmap="RdYlGn", norm=colors.CenteredNorm())
    plt.colorbar()
    plt.xticks(np.arange(len(y * 3)), y * 3, rotation=80)
    plt.yticks(np.arange(len(x)), x)
    # put x tick on top
    ax = plt.gca()
    ax.xaxis.tick_top()
    # plot a line to separate the groups
    plt.axvline(x=len(y) - 0.5, color='black')
    plt.axvline(x=len(y) * 2 - 0.5, color='black')
    # mark the groups on the bottom
    plt.text(len(y) / 2 - 0.5, 19, 'Heme', ha='center', va='center', fontsize=12)
    plt.text(len(y) * 1.5 - 0.5, 19, 'Sepsis', ha='center', va='center', fontsize=12)
    plt.text(len(y) * 2.5 - 0.5, 19, 'Sepsis + Heme', ha='center', va='center', fontsize=12)
    plt.show()


