#!/usr/bin/python
# -*- coding: utf-8 -*-
# TODO:
#    Add UI
#    Add 'Show in Google Maps'

import pygeoip
import csv

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['metro_code']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print 'Target:   ' + tgt
    print 'Location: '+str(city)+', '+str(region)+', '+str(country)
    print 'Latitude: '+str(lat)+ ', Longitude: '+ str(long) + '\n'


def main():
    with open('data.txt', 'rb') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            printRecord(row[0])
            
if __name__ == '__main__':
    main()
