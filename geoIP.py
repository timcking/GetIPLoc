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
        self.txtArea = xrc.XRCCTRL(self.frame, 'txtArea')
        self.txtZip = xrc.XRCCTRL(self.frame, 'txtZip')
        self.txtLatLon = xrc.XRCCTRL(self.frame, 'txtLatLon')
        self.txtLoc = xrc.XRCCTRL(self.frame, 'txtLoc')
        
        # Bind Events
        self.frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.listSummary)
        self.frame.Bind(wx.EVT_BUTTON, self.OnClose, id=xrc.XRCID('wxID_EXIT'))
        
        self.readLocFile()
        self.frame.Show()
    
    def readLocFile(self):
        self.index = 0
        # Read data from CSV (text) file
        with open('data.txt', 'rb') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                self.loadList(row[0], row[1], row[2])

    def loadList(self, tgt, theDate, theTime):
        # Load the list control
        self.listSummary.InsertStringItem(self.index, tgt)
        self.listSummary.SetStringItem(self.index, 1, theDate)
        self.listSummary.SetStringItem(self.index, 2, theTime)
        
        self.index += 1
    
    def showMap():
        # Hardcoded for now
        url = 'http://maps.google.com/?q=38.645,-121.4404'
        webbrowser.open_new(url)
            
    def OnClick(self, event):
        rec = self.gi.record_by_name(event.GetText())
        
        post_office = rec['postal_code']
        if post_office == None:
            post_office = ''
        
        self.txtArea.SetValue('%s' % (rec['area_code']))
        self.txtZip.SetValue('%s' % (post_office))
        self.txtLatLon.SetValue('%s,%s' % (str(rec['latitude']), str(rec['longitude'])))
        self.txtLoc.SetValue('%s, %s %s' % (rec['city'], rec['region_code'], rec['country_name']))
        
    def OnClose(self, evt):
        self.Exit()            
            
if __name__ == '__main__':
    # The False argument says redirect stdout/stderr to a console instead of a window
    app = MyApp(False)
    app.MainLoop()