#coding: UTF-8
import sys
import traceback
from pygmapslib import PyGMaps, PyGMapsError

__all__ = ['GeocodingError', 'Geocoding', 'request']

class NearestStationError(Exception):
    def __init__(self, error_status, params):
        self.error_status = error_status
        self.params = params

    def __str__(self):
        return self.error_status + '\n' + str(self.params)

    def __unicode__(self):
        return unicode(self.__str__())

class NearestStation(object):
    def __init__(self, data):
        self.data = data

    def __unicode__(self):
        names = ''
        for result in self.data:
            names = names + result['name'] + '\n'
        return names

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()

    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')

def get_nearest_station(location, key, sensor='false'):

    query_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    params = {
#Places APIはAPI key必須
        'key': key,
        'location' : str(location['lat']) + ',' + str(location['lng']),
        'sensor' : sensor,
#駅、地下鉄駅指定
        'types' : 'train_station|subway_station',
#距離順にソート 検索半径50km固定のみ
        'rankby' : 'distance',
#types指定のみだと鉄道会社の本社住所、切符販売所など駅でないものまで引っかかる
#とりあえずnameパラメータを指定することで凌ぐ
        'name' : 'station'
    }

    try:
#clientパラメータとsignatureはPlaces APIでは使用不可
        gmap_result = PyGMaps().get_data(query_url, params)

    except PyGMapsError as e:
        print traceback.format_exc()
        raise NearestStationError('HTTP STATUS ERROR', params)

    if gmap_result['status'] != 'OK':
        raise NearestStationError(gmap_result['status'], params)

    return NearestStation(gmap_result['results'])


