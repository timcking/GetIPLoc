#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygeoip
gi = pygeoip.GeoIP('GeoLiteCity.dat')


def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['metro_code']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print '[*] Target: ' + tgt + ' Geo-located. '
    print '[+] '+str(city)+', '+str(region)+', '+str(country)
    print '[+] Latitude: '+str(lat)+ ', Longitude: '+ str(long)


tgt = '66.249.76.164'
printRecord(tgt)

