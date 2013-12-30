# -*- coding: utf-8 -*-
# TODO:
#    Add UI
#    Add 'Show in Google Maps'
#      maps query: http://maps.google.com/?q=38.645,-121.4404

import wx
from wx import xrc
import pygeoip
import csv
import webbrowser

class MyApp(wx.App):
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    
    def OnInit(self):
        # Read data from CSV (text) file
        with open('data.txt', 'rb') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                self.getLocData(row[0], row[1])
                
        self.res = xrc.XmlResource('GetIPLoc.xrc')
        self.init_frame()
        return(True)

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frameMain')
        self.frame.Show()
        
        # Bind Controls
        self.btnExit = xrc.XRCCTRL(self.frame, 'wxID_EXIT')
        
        # Bind Events
        self.frame.Bind(wx.EVT_BUTTON, self.OnClose, id=xrc.XRCID('wxID_EXIT'))

    def getLocData(self, tgt, date):
        rec = self.gi.record_by_name(tgt)
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
    
    def showMap():
        # Hardcoded for now
        url = 'http://maps.google.com/?q=38.645,-121.4404'
        webbrowser.open_new(url)
            
    def OnClose(self, evt):
        self.Exit()            
            
if __name__ == '__main__':
    # The False argument says redirect stdout/stderr to a console instead of a window
    app = MyApp(False)
    app.MainLoop()