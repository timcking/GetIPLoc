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
    dictLocs = {}
    
    def OnInit(self):
        self.res = xrc.XmlResource('GetIPLoc.xrc')
        self.init_frame()
        return(True)

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frameMain')
        
        # Bind Controls
        self.btnExit = xrc.XRCCTRL(self.frame, 'wxID_EXIT')
        self.listSummary = xrc.XRCCTRL(self.frame, 'listSummary')
        self.listSummary.InsertColumn(0, 'IP', width=110)
        self.listSummary.InsertColumn(1, 'Date')
        self.listSummary.InsertColumn(2, 'Time')        
        
        # Bind Events
        self.frame.Bind(wx.EVT_BUTTON, self.OnClose, id=xrc.XRCID('wxID_EXIT'))
        
        self.readLocFile()
        self.frame.Show()
    
    def readLocFile(self):
        self.index = 0
        # Read data from CSV (text) file
        with open('data.txt', 'rb') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                self.getLocData(row[0], row[1], row[2])

    def getLocData(self, tgt, theDate, theTime):
        # Load the list control
        self.listSummary.InsertStringItem(self.index, tgt)
        self.listSummary.SetStringItem(self.index, 1, theDate)
        self.listSummary.SetStringItem(self.index, 2, theTime)
        
        rec = self.gi.record_by_name(tgt)
        city = rec['city']
        region = rec['metro_code']
        country = rec['country_name']
        lon = rec['longitude']
        lat = rec['latitude']
        
        # Save to dict here
        #index_count = 0
        #for theRec in rec:
            #try:
                #self.listSummary.Append("%s, %s %s" % (tgt, theDate, theTime))
            #except Exception, e:
                #print "Change me"
            
            # Save for when box is clicked
            #self.dictTitles[index_count] = title.movieID
            #index_count += 1         
        
        print 'IP Addr:   ' + tgt
        print 'Date/Time: ' + theDate + ' ' + theTime
        print 'Location:  ' + str(city)+', '+ str(region)+', '+ str(country)
        print 'Lat/Lon:   ' + str(lat) + ','+ str(lon)
        print ''
        
        self.index += 1
    
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