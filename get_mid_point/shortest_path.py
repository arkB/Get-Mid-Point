# -*- coding:utf-8 -*-
import pandas as pd
import networkx as nx
from pyproj import Geod


class ShortestPath(object):
    """docstring for ShortestPath"""
    def __init__(self, station_file, line_file, join_file):
        super(ShortestPath, self).__init__()
        self.station_file = station_file
        self.line_file = line_file
        self.join_file = join_file
        self.station_df = pd.read_csv(station_file)
        self.line_df = pd.read_csv(line_file)
        self.join_df = pd.read_csv(join_file)
        self.rail_net = self._make_rail_net()

    def shortest_path_name(self, from_station_name, to_station_name):
        '''
        return shortest path in station_name.
        '''
        shortest_path =\
            self.shortest_path(
                from_station_name,
                to_station_name)
        return [self.station_df[self.station_df['station_g_cd']
                == gcd]['station_name'] for gcd in shortest_path]

    def shortest_path(self, from_station_name, to_station_name):
        '''
        Return shortest path.
        '''
        from_station_g_cd = self._station_name_gcd(from_station_name)
        to_station_g_cd = self._station_name_gcd(to_station_name)
        shortest_path =\
            nx.dijkstra_path(
                self.rail_net,
                from_station_g_cd,
                to_station_g_cd)
        return shortest_path

    def shortest_path_with_locations(self, from_station_location,
                                     to_station_location):
        '''
        Return shortest path with two station locations.
        '''
        from_station_g_cd = self._station_location_gcd(from_station_location)
        to_station_g_cd = self._station_location_gcd(to_station_location)
        shortest_path =\
            nx.dijkstra_path(
                self.rail_net,
                from_station_g_cd,
                to_station_g_cd)
        return shortest_path

    def shortest_path_length(self, from_station_name, to_station_name):
        '''
        Return shortest path length.
        '''
        from_station_g_cd = self._station_name_gcd(from_station_name)
        to_station_g_cd = self._station_name_gcd(to_station_name)
        shortest_path_length =\
            nx.dijkstra_path_length(
                self.rail_net,
                from_station_g_cd,
                to_station_g_cd)
        return shortest_path_length

    def shortest_path_length_with_locations(self,
                                            from_station_location,
                                            to_station_location):
        '''
        Return shortest path length with two locations of station.
        '''
        from_station_g_cd = self._station_location_gcd(from_station_location)
        to_station_g_cd = self._station_location_gcd(to_station_location)
        shortest_path_length =\
            nx.dijkstra_path_length(
                self.rail_net,
                from_station_g_cd,
                to_station_g_cd)
        return shortest_path_length

    def _station_name_gcd(self, station_name):
        '''
        Return gcd of station_name.
        if station can't be identified, Raising Error.
        '''
        station_gcds =\
            self.station_df[self.station_df['station_name']
                            == station_name]['station_g_cd'].unique()
        if len(station_gcds) > 1:
            raise ValueError(
                'there is more than one candidate with station_name:{}'
                .format(station_name))
        elif len(station_gcds) == 0:
            raise ValueError(
                'there is no candidate statioon_name:{}'
                .format(station_name))
        return int(station_gcds)

    def _station_location_gcd(self, station_location):
        '''
        Return gcd of station_location.
        if station can't be identified, Raising Error.
        '''
        error = 0.002
        station_gcds =\
            self.station_df[
                abs(self.station_df['lat']
                    -
                    float(station_location['lat'])) < error
            ][
                abs(self.station_df['lon']
                    -
                    float(station_location['lng'])) < error
            ]['station_g_cd'].unique()
        if len(station_gcds) > 1:
            raise ValueError('there is more than one candidate of'
                             + 'station_location:{}'
                             .format(station_location))
        elif len(station_gcds) == 0:
            raise ValueError('there is no candidate of'
                             + 'station_location:{}'
                             .format(station_location))
        return int(station_gcds)

    def _make_rail_net(self):
        '''
        Making nx.Graph of rail net.
        '''
        rail_net = nx.Graph()
        for station in self.station_df['station_g_cd']:
            rail_net.add_node(station)
        all_edges = self._make_all_edges()
        for edge in all_edges:
            rail_net.add_edge(edge[0], edge[1], weight=edge[2])
        return rail_net.copy()

    def _make_all_edges(self):
        '''
        make all of edges
        '''
        all_edges = set([])
        for line_cd in self.line_df['line_cd']:
            all_edges =\
                all_edges.union(set(self._edges_in_line(line_cd)))
        return all_edges

    def _edges_in_line(self, line_cd):
        '''
        Return edges in the line.
        Supporsing the edge connectiong
        the station and the next station.
        '''
        stations = self._stations_in_linecd(line_cd)
        edges = []
        for i in stations.index:
            try:
                start_cd = stations['station_g_cd'][i]
                to_cd = stations['station_g_cd'][i + 1]
                start = {'lon': stations['lon'][i],
                         'lat': stations['lat'][i]}
                to = {'lon': stations['lon'][i + 1],
                      'lat': stations['lat'][i + 1]}
                distance = self._distance(start, to)
                edges.append((start_cd, to_cd, distance))
            except KeyError:
                continue
        return edges

    def _stations_in_linecd(self, line_cd):
        '''
        Return DataFrame of stations in line_cd.
        '''
        return self.station_df[self.station_df['line_cd'] == line_cd]

    def _distance(self, start, to):
        '''
        Return distance.
        '''
        q = Geod(ellps='WGS84')
        fa, ba, d =\
            q.inv(start['lon'],
                  start['lat'],
                  to['lon'],
                  to['lat'])
        return d
