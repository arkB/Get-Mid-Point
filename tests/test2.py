#coding: UTF-8
#Geographic midpoint
#http://www.geomidpoint.com/meet/
#http://www.geomidpoint.com/calculation.html
from math import (pi, sin, cos, atan2, sqrt)
from get_mid_point import (pygmapslib, directions, geocoding, placesearch)

def get_middle_point(coordinates):
    x = 0
    y = 0
    z = 0
    for point in coordinates:
        x = x + cos(point['lat'] * pi / 180) * cos(point['lng'] * pi /180)
        y = y + cos(point['lat'] * pi / 180) * sin(point['lng'] * pi /180)
        z = z + sin(point['lat'] * pi / 180)
    x = x / len(coordinates)
    y = y / len(coordinates)
    z = z / len(coordinates)
    return {'lng' : atan2(y,x) * 180 / pi, 'lat' : atan2(z, sqrt(x*x + y*y)) * 180 /pi}

point1 = geocoding.request('Tokyo station')
point2 = geocoding.request('Ikebukuro station')
point3 = geocoding.request('Shibuya station')
middle_cord = get_middle_point([point1.data[0]['geometry']['location'], point2.data[0]['geometry']['location'], point3.data[0]['geometry']['location']])
stations = placesearch.get_nearest_station(middle_cord, key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

print stations

