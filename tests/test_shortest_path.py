# -*- coding:utf-8 -*-
from get_mid_point import shortest_path
LINE_FILE = './train_data/line20140303free.csv'
STATION_FILE = './train_data/station20140303free.csv'
JOIN_FILE = './train_data/join20140303.csv'


def test_shortest_path():
    sp = shortest_path.ShortestPath(STATION_FILE,
                                    LINE_FILE,
                                    JOIN_FILE)
    print sp.shortest_path_name('青森', '東京')
    assert True

if __name__ == '__main__':
    LINE_FILE = '../train_data/line20140303free.csv'
    STATION_FILE = '../train_data/station20140303free.csv'
    JOIN_FILE = '../train_data/join20140303.csv'
    test_shortest_path()
