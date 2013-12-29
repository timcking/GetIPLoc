# -*- coding: utf-8 -*-
# TODO:
#    Add UI
#    Add 'Show in Google Maps'
#      maps query: http://maps.google.com/?q=38.645,-121.4404

import pygeoip
import csv
import webbrowser

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def printRecord(tgt, date):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['metro_code']
    country = rec['country_name']
    lon = rec['longitude']
    lat = rec['latitude']
    print 'IP Addr:  ' + tgt
    print 'Date:     ' + date
    print 'Location: '+ str(city)+', '+ str(region)+', '+ str(country)
    print 'Lat/Lon:  ' + str(lat) + ','+ str(lon)
    print ''

def main():
    with open('data.txt', 'rb') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            printRecord(row[0], row[1])
            
    # Test open Google maps
    #url = 'http://maps.google.com/?q=38.645,-121.4404'
    #webbrowser.open_new(url)
            
if __name__ == '__main__':
    main()
