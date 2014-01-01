# -*- coding: utf-8 -*-
# TODO:
#    Get (scrape?) loc data directly from web page
#    Move code out of list OnClick event

import wx
from wx import xrc
import pygeoip
import csv
import webbrowser

class MyApp(wx.App):
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    rec = []
    
    def OnInit(self):
        self.res = xrc.XmlResource('GetIPLoc.xrc')
        self.init_frame()
        return(True)

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frameMain')
        
        # Bind Controls
        self.btnExit = xrc.XRCCTRL(self.frame, 'wxID_EXIT')
        self.btnMap = xrc.XRCCTRL(self.frame, 'btnMap')
        self.listSummary = xrc.XRCCTRL(self.frame, 'listSummary')
        self.listSummary.InsertColumn(0, 'IP', width=100)
        self.listSummary.InsertColumn(1, 'Date', width=90)
        self.listSummary.InsertColumn(2, 'Time', width=90)        
        self.txtArea = xrc.XRCCTRL(self.frame, 'txtArea')
        self.txtZip = xrc.XRCCTRL(self.frame, 'txtZip')
        self.txtLatLon = xrc.XRCCTRL(self.frame, 'txtLatLon')
        self.txtLoc = xrc.XRCCTRL(self.frame, 'txtLoc')
        
        # Bind Events
        self.frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.listSummary)
        self.frame.Bind(wx.EVT_BUTTON, self.OnClose, id=xrc.XRCID('wxID_EXIT'))
        self.frame.Bind(wx.EVT_BUTTON, self.OnClickMap, id=xrc.XRCID('btnMap'))
        
        self.readLocFile()
        self.frame.Show()
    
    def readLocFile(self):
        self.index = 0
        # Read data from CSV (text) file
        with open('data.txt', 'rb') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                self.loadList(row[0], row[1], row[2])

    def loadList(self, theLoc, theDate, theTime):
        # Load the list control
        self.listSummary.InsertStringItem(self.index, theLoc)
        self.listSummary.SetStringItem(self.index, 1, theDate)
        self.listSummary.SetStringItem(self.index, 2, theTime)
        
        self.index += 1
        
    def loadRec(self, theLoc):
        self.rec = self.gi.record_by_name(theLoc)
        
        post_office = self.rec['postal_code']
        if post_office == None:
            post_office = ''
        
        self.txtArea.SetValue('%s' % (self.rec['area_code']))
        self.txtZip.SetValue('%s' % (post_office))
        self.txtLatLon.SetValue('%s,%s' % (str(self.rec['latitude']), str(self.rec['longitude'])))
        self.txtLoc.SetValue('%s, %s %s' % (self.rec['city'], self.rec['region_code'], self.rec['country_name']))
    
    def OnClick(self, event):
        self.loadRec(event.GetText())
        
    def OnClose(self, evt):
        self.Exit()            
            
    def OnClickMap(self, evt):
        url = 'http://maps.google.com/?q=' + str(self.rec['latitude']) + ',' + str(self.rec['longitude'])
        webbrowser.open_new(url)
        
if __name__ == '__main__':
    # The False argument says redirect stdout/stderr to a console instead of a window
    app = MyApp(False)
    app.MainLoop()