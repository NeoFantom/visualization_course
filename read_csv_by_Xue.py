import pandas as pd
import os
from io import StringIO
import networkx as nx
import logging


def x_get_all_data_enhanced(from_path: str, file_name: str, days=30):
    """

    :param from_path: the directory containing a month of data, without an
    ending '/' or '\\'
    :param file_name: the file you want to read in every day
    :param days: how many days of data you want to read, default 30
    :return: an object of pandas.DataFrame
    """
    df = None
    s = ''
    for i in range(1, 1 + days):
        path = from_path + '/2017-11-' + '{0:0>2d}'.format(i) + '/'
        with open(path + file_name, mode='r', encoding='gbk') as f:
            print('Reading file \"' + path + file_name + '\"... ', flush=True)

            line = f.readline()
            s += line
            line_number = 1
            while line:
                try:
                    line = f.readline()
                    line_number += 1
                    cells = line.split(',')
                    if (len(cells) < 9) or ('@' not in cells[6]) or ('@' not in cells[7]):
                        continue  # Bad data or end of file
                    else:  # Correct row of data
                        s += line
                except UnicodeDecodeError:
                    print('\tBad data at line', str(line_number), 'of file ', path, file_name, flush=True)
                    line = 'place_holder'

        df = pd.concat([df, pd.read_csv(StringIO(s), dtype=str)], ignore_index=True)
        print('done', flush=True)
        s = ''

    return df


def pre_process(from_path: str, file_name: str, days=30):
    """

    :param from_path: the directory containing a month of data, without an
    ending '/' or '\\'
    :param file_name: the file you want to read in every day
    :param days: how many days of data you want to read, default 30
    :return: an object of pandas.DataFrame
    """
    s = ''
    for i in range(1, 1 + days):
        path = from_path + '/2017-11-' + '{0:0>2d}'.format(i) + '/'
        with open(path + file_name, mode='r', encoding='gbk') as f:
            print('Reading file \"' + path + file_name + '\"... ', flush=True)

            line = f.readline()
            s += line
            line_number = 1
            while line:
                try:
                    line = f.readline()
                    line_number += 1
                    cells = line.split(',')
                    if (len(cells) < 9) or ('@' not in cells[6]) or ('@' not in cells[7]):
                        continue  # Bad data or end of file
                    else:  # Correct row of data
                        s += line
                except UnicodeDecodeError:
                    print('\tBad data at line', str(line_number), 'of file ', path, file_name, flush=True)
                    line = 'place_holder'

        print(s[:1000])
        # if input('Write? [y/n]') == 'y':
        with open(path + file_name, mode='w', encoding='utf-8') as f:
            if not f.write(s):
                print('Write failed.')
            else:
                print('Write success.')

        print('done', flush=True)
        s = ''

    return


def _test_read_data():
    with open('data/2017-11-01/email.csv', encoding='gbk') as f:
        s = f.read()
        df = pd.read_csv(StringIO(s), dtype=str)
        print(df.tail())
    # df = pd.read_csv('data/2017-11-01/email.csv', encoding='gbk')
    # print(df.head(10))
    return


def x_get_all_data(from_path: str, file_name: str, days=30):
    """

    :param from_path: the directory containing a month of data, without an
    ending '/' or '\\'
    :param file_name: the file you want to read in every day
    :param days: how many days of data you want to read, default 30
    :return: an object of pandas.DataFrame
    """
    df = None
    for i in range(1, 1 + days):
        path = from_path + '/2017-11-' + '{0:0>2d}'.format(i) + '/'
        print('Reading file \"' + path + file_name + '\"... ', flush=True)
        one_day_data = pd.read_csv(path + file_name)
        df = pd.concat([df, one_day_data], ignore_index=True)
        print('\t', df.tail())
        print('done', flush=True)
    return df


if __name__ == '__main__':

    def test():
        pre_process('data', 'email.csv', days=30)
        return

    def get_relationship_graph_from_emails():
        email_graph: nx.Graph = nx.Graph()
        email_graph.clear()

        df: pd.DataFrame = x_get_all_data('data', 'email.csv', days=30)

        edges_info = {}
        nodes_info = {}
        for row in df.itertuples(False):
            fr: str = row._6
            tos: str = row.to
            try:
                for to in row.to.split(';'):
                    nodes_info[fr] = nodes_info.get(fr, 0) + 1
                    nodes_info[to] = nodes_info.get(to, 0) + 1
                    from_to = (fr, to)
                    edges_info[from_to] = edges_info.get(from_to, 0) + 1
            except AttributeError as e:
                logging.error(e)
                print(row)
                exit()

        nodes_list = list(nodes_info.keys())
        for email in nodes_info.keys():
            email_graph.add_node(nodes_list.index(email), weight=nodes_info[email], label=email)
        for from_to in edges_info.keys():
            email_graph.add_edge(nodes_list.index(from_to[0]),
                                 nodes_list.index(from_to[1]),
                                 weight=edges_info[from_to])

        nx.write_gexf(email_graph, 'result/email.gexf')
        return
