#!/usr/bin/python
'''
Created on Nov 22, 2011

@author: Vikas Sakode
'''

#import re;
import commands;
import os;
#import datetime;
import time;
import sys;
import MySQLdb as mdb
from pychart import *

theme.get_options()

def usage():
    print "Usage:", sys.argv[0], ' logfileName'
    sys.exit()

def format_date(ordinal):
    return "/a90{}" + time.ctime(int(ordinal))

def validateyear(yr):
    if len(yr) != 4:
        return False
    else:
        return True
        

def checkyear(nfile):
    getfirstline = "head -1 " + nfile
    fline = commands.getoutput(getfirstline)
    mline = fline.split()
    if mline[6] != "2011":
        print "Missing year in date timestamp"
        nyear = getyear()
    return nyear

def getSite(nfile):
    sitetoken = "head -1 " + nfile + "| awk '{print $7}' | cut -d '-' -f 1"
    token = commands.getoutput(sitetoken)
    return token

def chkyr(xdate):
    yr = xdate.split("-")[0]
    #print yr
    if len(yr) == 4 and yr.isdigit():
        return True
    else:
        return False
    
def chkmon(xdate):
    mon = xdate.split("-")[1]
    #print mon
    if len(mon) == 2 and mon.isdigit() and int(mon) < 13:
        return True
    else:
        return False
    
def chkdt(xdate):
    dt = xdate.split("-")[2]
    #print dt
    if len(dt) == 2 and dt.isdigit() and int(dt) < 32:
        return True
    else:
        return False
        
def validateDate(xdate):
    if len(xdate) != 10:
        return False
    elif chkyr(xdate) and chkmon(xdate) and chkdt(xdate):
        return True
    else:
        return False
        
        
def getStartDate():
    print "Enter the start date to select the data (YYYY-MM-DD)"
    ndate = raw_input()
    if not ndate:
        print "##### Cannot be NULL #####"
        dt = getStartDate()
        return dt
    elif validateDate(ndate):
        dt = ndate
        return dt
    else:
        print "Invalid date"
        dt = getStartDate()
        return dt        
 
def getEndDate():
    print "Enter the end date to select the data (YYYY-MM-DD)"
    ndate = raw_input()
    if not ndate:
        print "##### Cannot be NULL #####"
        dt = getStartDate()
        return dt
    elif validateDate(ndate):
        dt = ndate
        return dt
    else:
        print "Invalid date"
        dt = getEndDate()
        return dt        
           
def getyear():
    print "Enter the year (YYYY)[Default : 2011] :"
    nyear = raw_input()
    if not nyear:
        year = "2011"
        return year
    elif validateyear(nyear) and nyear.isdigit():
        year = nyear
        return year
    else:
        print "Invalid year"
        yr3 = getyear()
        return yr3

def validatecho(ch):
    if len(ch) == 1:
        return True
    else:
        return False
    
def getchoice():
    print "Enter your choice (n) [Default:3]: "
    ch = raw_input();
    if not ch:
        cho = "3"
        return cho
    elif validatecho(ch) and ch.isdigit():
        cho = ch
        return ch
    else:
        print "Invalid number"
        cho = getchoice()
        return cho

def plotData(name, data, voltest_data, svgout):
    os.chdir('./output/graphs')            
    can = canvas.init(svgout)
    drawn = 0
    size = (3600, 800)
    if len(data) != 0:
        print "Plotting vol1 data"
        ar = area.T(legend=legend.T(loc=(3610,100)),size = size,
                    x_coord= category_coord.T(data,0),
                    y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Data Transfered ( GB )"))
        ar.add_plot(bar_plot.T(label="Data",data=data))
        ar.draw()
        can.set_author("Vikas Sakode")
        ar.draw(can)
        title = name + " SnapMirror Performance "
        tb = text_box.T(fill_style=fill_style.gray90,loc=(1600,820),text="/32/C" + title, line_style=None)    
        tb.draw(can)
        drawn = 1
    else:
        print "******NO 'vol1' data to plot"
        
    
    if len(voltest_data) != 0:
        print "Plotting voltest data"
        ar = area.T( loc=(3700, 0), legend=legend.T(loc=(4910,100)),size = (1200,800),
                    x_coord= category_coord.T(voltest_data,0),
                    #y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Data Transfered ( GB )"))
        ar.add_plot(bar_plot.T(label="Data",data=voltest_data))
        ar.draw()
        tb1 = text_box.T(fill_style=fill_style.gray90,loc=(2000,620),text="/52/C" + "vol1", line_style=None)
        tb2 = text_box.T(fill_style=fill_style.gray90,loc=(4600,620),text="/52/C" + "voltest", line_style=None)
        tb1.draw(can)
        tb2.draw(can)
        drawn = 1
    else:
        print "******NO 'voltest' data to plot"
    
    if drawn == 0:
        print "######NO data to plot in the specified date range... Please update the database....#######"
    else:
        print 'Script completed successfully'
        #print '[INFO] Data file ' + dataout + ' is created in output/data directory'
        print '[INFO] SVG Graph file ' + svgout + ' is created in output/graphs directory.'
        print '       Best viewed in CHROME Browser'
            
    
def plotSpeed(name, transferspeed, voltest_transferspeed, svgout):
    os.chdir('./output/graphs')            
    can = canvas.init(svgout)
    drawn = 0
    size = (3600, 800)
    if len(transferspeed)!= 0:
        print "Plotting vol1 data"
        ar = area.T(legend=legend.T(loc=(3650,100)),size = size,
                    x_coord= category_coord.T(transferspeed,0),
                    #y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Speed ( Mbps )"))
        ar.add_plot(line_plot.T(label="Speed",data=transferspeed))
        ar.draw()
        can.set_author("Vikas Sakode")
        ar.draw(can) 
        title = name + " SnapMirror Performance "
        tb = text_box.T(fill_style=fill_style.gray90,loc=(1600,820),text= "/32/C" + title, line_style=None)
        tb.draw(can)
        drawn = 1
    else:
        print "******NO 'vol1' data to plot"
                
    if len(voltest_transferspeed) != 0:
        print "Plotting voltest data"
        ar = area.T( loc=(3700, 0), legend=legend.T(loc=(4910,100)),size = (1200,800),
                    x_coord= category_coord.T(voltest_transferspeed,0),
                    #y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Speed ( Mbps )"))
        ar.add_plot(line_plot.T(label="Speed",data=voltest_transferspeed))
        ar.draw()
        tb1 = text_box.T(fill_style=fill_style.gray90,loc=(2000,620),text="/52/C" + "vol1", line_style=None)
        tb2 = text_box.T(fill_style=fill_style.gray90,loc=(4600,620),text="/52/C" + "voltest", line_style=None)
        tb1.draw(can)
        tb2.draw(can)
        drawn = 1
    else:
        print "******NO 'voltest' data to plot"
    
    if drawn == 0:
        print "######NO data to plot in the specified date range... Please update the database....#######"
    else:
        print 'Script completed successfully'
        #print '[INFO] Data file ' + dataout + ' is created in output/data directory'
        print '[INFO] SVG Graph file ' + svgout + ' is created in output/graphs directory.'
        print '       Best viewed in CHROME Browser'
        
def plotDataTime(name, data, transfertime, voltest_data, voltest_transfertime, svgout):
    os.chdir('./output/graphs')    
    drawn = 0        
    can = canvas.init(svgout)
    size = (3600, 800)
    
    if len(data):
        ar = area.T(legend=legend.T(loc=(3650,100)),size = size,
                    x_coord= category_coord.T(data,0),
                    y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Data Transfered ( GB )"))
        ar.add_plot(bar_plot.T(label="Data",data=data))
        ar.draw()
        ar = area.T(legend=legend.T(loc=(3650,120)), size=size,
                    x_coord= category_coord.T(transfertime,0),
                    x_axis = None, 
                    #y_grid_interval=500,
                    y_axis2 = axis.Y(offset=3600, label = "/20/C" +"Transfer Time ( Min )", draw_tics_right=1))
                    #y_axis = axis.Y(offset=300,
                    #                label_offset=(10, 0), label="Speed"))
        ar.add_plot(line_plot.T(line_style=line_style.blue, label="Time",data=transfertime, data_label_offset = (10,10), data_label_format = "/a45/8{}%d", tick_mark=tick_mark.x3))
        ar.draw()
        can.set_author("Vikas Sakode")
        ar.draw(can)
        title = name + " SnapMirror Performance "
        tb = text_box.T(fill_style=fill_style.gray90,loc=(1600,820),text="/32/C" +title, line_style=None)
        tb.draw(can)
        drawn = 1
    else:
        print "******NO 'vol1' data to plot"
                
        
    if len(voltest_data):
        ar = area.T(loc = (3700,0), legend=legend.T(loc=(4950,100)),size = (1200,800),
                    x_coord= category_coord.T(voltest_data,0),
                    #y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Data Transfered ( GB )"))
        ar.add_plot(bar_plot.T(label="Data",data=voltest_data))
        ar.draw()
        
        ar = area.T(loc = (3700,0), legend=legend.T(loc=(4950,120)), size= (1200,800),
                    x_coord= category_coord.T(voltest_transfertime,0),
                    x_axis = None, 
                    #y_grid_interval=500,
                    y_axis2 = axis.Y(offset=1200, label = "/20/C" +"Transfer Time ( Min )", draw_tics_right=1))
                    #y_axis = axis.Y(offset=300,
                    #                label_offset=(10, 0), label="Speed"))
        ar.add_plot(line_plot.T(line_style=line_style.blue, label="Time",data=voltest_transfertime, data_label_offset = (10,10), data_label_format = "/a45/8{}%d", tick_mark=tick_mark.x3))
        ar.draw()
        tb1 = text_box.T(fill_style=fill_style.gray90,loc=(2000,620),text="/52/C" + "vol1", line_style=None)
        tb2 = text_box.T(fill_style=fill_style.gray90,loc=(4600,620),text="/52/C" + "voltest", line_style=None)
        tb1.draw(can)
        tb2.draw(can)
        drawn = 1
    else:
        print "******NO 'voltest' data to plot"
    
    if drawn == 0:
        print "######NO data to plot in the specified date range... Please update the database....#######"
    else:
        print 'Script completed successfully'
        #print '[INFO] Data file ' + dataout + ' is created in output/data directory'
        print '[INFO] SVG Graph file ' + svgout + ' is created in output/graphs directory.'
        print '       Best viewed in CHROME Browser'
        
def plotBoth(name, data, transferspeed, voltest_data, voltest_transferspeed, svgout):
    os.chdir('./output/graphs')    
    drawn = 0        
    can = canvas.init(svgout)
    size = (3600, 800)
    
    if len(data):
        ar = area.T(legend=legend.T(loc=(3650,100)),size = size,
                    x_coord= category_coord.T(data,0),
                    y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Data Transfered ( GB )"))
        ar.add_plot(bar_plot.T(label="Data",data=data))
        ar.draw()
        ar = area.T(legend=legend.T(loc=(3650,120)), size=size,
                    x_coord= category_coord.T(transferspeed,0),
                    x_axis = None, 
                    #y_grid_interval=500,
                    y_axis2 = axis.Y(offset=3600, label = "/20/C" +"Transfer Speed ( Mbps )", draw_tics_right=1))
                    #y_axis = axis.Y(offset=300,
                    #                label_offset=(10, 0), label="Speed"))
        ar.add_plot(line_plot.T(line_style=line_style.blue, label="Speed",data=transferspeed, tick_mark=tick_mark.x3))
        ar.draw()
        can.set_author("Vikas Sakode")
        ar.draw(can)
        title = name + " SnapMirror Performance "
        tb = text_box.T(fill_style=fill_style.gray90,loc=(1600,820),text="/32/C" +title, line_style=None)
        tb.draw(can)
        drawn = 1
    else:
        print "******NO 'vol1' data to plot"
                
        
    if len(voltest_data):
        ar = area.T(loc = (3700,0), legend=legend.T(loc=(4950,100)),size = (1200,800),
                    x_coord= category_coord.T(voltest_data,0),
                    #y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="/20/C" +"Date"),
                    y_axis = axis.Y(label="/20/C" +"Data Transfered ( GB )"))
        ar.add_plot(bar_plot.T(label="Data",data=voltest_data))
        ar.draw()
        
        ar = area.T(loc = (3700,0), legend=legend.T(loc=(4950,120)), size= (1200,800),
                    x_coord= category_coord.T(voltest_transferspeed,0),
                    x_axis = None, 
                    #y_grid_interval=500,
                    y_axis2 = axis.Y(offset=1200, label = "/20/C" +"Transfer Speed ( Mbps )", draw_tics_right=1))
                    #y_axis = axis.Y(offset=300,
                    #                label_offset=(10, 0), label="Speed"))
        ar.add_plot(line_plot.T(line_style=line_style.blue, label="Speed",data=voltest_transferspeed, tick_mark=tick_mark.x3))
        ar.draw()
        tb1 = text_box.T(fill_style=fill_style.gray90,loc=(2000,620),text="/52/C" + "vol1", line_style=None)
        tb2 = text_box.T(fill_style=fill_style.gray90,loc=(4600,620),text="/52/C" + "voltest", line_style=None)
        tb1.draw(can)
        tb2.draw(can)
        drawn = 1
    else:
        print "******NO 'voltest' data to plot"
    
    if drawn == 0:
        print "######NO data to plot in the specified date range... Please update the database....#######"
    else:
        print 'Script completed successfully'
        #print '[INFO] Data file ' + dataout + ' is created in output/data directory'
        print '[INFO] SVG Graph file ' + svgout + ' is created in output/graphs directory.'
        print '       Best viewed in CHROME Browser'
        
    
def getSiteName():
    print "Select Site : "
    print "1) us01"
    print "2) hu01"
    print "3) de02"
    print "4) ie02"   
    print "Enter your choice (n) [Default:1]: "
    ch = raw_input();
    if not ch:
        cho = "1"
        return int(cho)
    elif validatecho(ch) and ch.isdigit():
        return int(ch)
    else:
        print "Invalid number"
        cho = getSiteName()
        return int(cho)  
    
def main(): 
    site = 0
    while int(site) not in [1,2,3,4]:
        site = getSiteName()
        
    sdt = getStartDate();
    edt = getEndDate();
    outfile = "snapmirror." + str(int(time.time()))
    svgout = outfile + ".svg"
    
    data = []
    transferspeed = []
    transfertime = []
    voltest_data = []
    voltest_transferspeed = []
    voltest_transfertime = []
    sitename = "us01"
    con = None
    if site == 1:
        sitename = "us01"
        try:
            con = mdb.connect('bassql1', 'estsnapmirror', 'estsnapmirror#', 'estsnapmirror')
            cur = con.cursor()
            cur.execute("""SELECT  start_timestamp, data_transfered from us01 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            numrowsdata = int(cur.rowcount);
            for i in range(numrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from us01 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowsspeed = int(cur.rowcount);
            for i in range(numrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                transferspeed.append(speedpair)
            
            cur.execute("""SELECT  start_timestamp, transfer_time from us01 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowstime = int(cur.rowcount);
            for i in range(numrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                transfertime.append(timepair)
            
            cur.execute("""SELECT  start_timestamp, data_transfered from us01 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            vnumrowsdata = int(cur.rowcount);
            for i in range(vnumrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                voltest_data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from us01 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowsspeed = int(cur.rowcount);
            for i in range(vnumrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                voltest_transferspeed.append(speedpair)
                
            
            cur.execute("""SELECT  start_timestamp, transfer_time from us01 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowstime = int(cur.rowcount);
            for i in range(vnumrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                voltest_transfertime.append(timepair)
            
        except mdb.Error,e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
       
    elif site == 2:
        sitename = "hu01"
        try:
            con = mdb.connect('bassql1', 'estsnapmirror', 'estsnapmirror#', 'estsnapmirror')
            cur = con.cursor()
            cur.execute("""SELECT  start_timestamp, data_transfered from hu01 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            numrowsdata = int(cur.rowcount);
            for i in range(numrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from hu01 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowsspeed = int(cur.rowcount);
            for i in range(numrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                transferspeed.append(speedpair)
                
            
            cur.execute("""SELECT  start_timestamp, transfer_time from hu01 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowstime = int(cur.rowcount);
            for i in range(numrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                transfertime.append(timepair)
                
            cur.execute("""SELECT  start_timestamp, data_transfered from hu01 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            vnumrowsdata = int(cur.rowcount);
            for i in range(vnumrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                voltest_data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from hu01 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowsspeed = int(cur.rowcount);
            for i in range(vnumrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                voltest_transferspeed.append(speedpair)
                
            
            cur.execute("""SELECT  start_timestamp, transfer_time from hu01 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowstime = int(cur.rowcount);
            for i in range(vnumrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                voltest_transfertime.append(timepair)
            
        except mdb.Error,e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        
    elif site == 3:
        sitename = "de02"
        try:
            con = mdb.connect('bassql1', 'estsnapmirror', 'estsnapmirror#', 'estsnapmirror')
            cur = con.cursor()
            cur.execute("""SELECT  start_timestamp, data_transfered from de02 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            numrowsdata = int(cur.rowcount);
            for i in range(numrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from de02 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowsspeed = int(cur.rowcount);
            for i in range(numrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                transferspeed.append(speedpair)
                
            
            cur.execute("""SELECT  start_timestamp, transfer_time from de02 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowstime = int(cur.rowcount);
            for i in range(numrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                transfertime.append(timepair)
                
            cur.execute("""SELECT  start_timestamp, data_transfered from de02 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            vnumrowsdata = int(cur.rowcount);
            for i in range(vnumrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                voltest_data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from de02 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowsspeed = int(cur.rowcount);
            for i in range(vnumrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                voltest_transferspeed.append(speedpair)
            
            
            cur.execute("""SELECT  start_timestamp, transfer_time from de02 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowstime = int(cur.rowcount);
            for i in range(vnumrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                voltest_transfertime.append(timepair)
            
        except mdb.Error,e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        
       
        
    else:
        sitename = "ie02"
        try:
            con = mdb.connect('bassql1', 'estsnapmirror', 'estsnapmirror#', 'estsnapmirror')
            cur = con.cursor()
            cur.execute("""SELECT  start_timestamp, data_transfered from ie02 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            numrowsdata = int(cur.rowcount);
            for i in range(numrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from ie02 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowsspeed = int(cur.rowcount);
            for i in range(numrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                transferspeed.append(speedpair)
                
            
            cur.execute("""SELECT  start_timestamp, transfer_time from ie02 WHERE volume="vol1" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            numrowstime = int(cur.rowcount);
            for i in range(numrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                transfertime.append(timepair)
                
            cur.execute("""SELECT  start_timestamp, data_transfered from ie02 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            #cur.fetchall();
            vnumrowsdata = int(cur.rowcount);
            for i in range(vnumrowsdata):
                row = cur.fetchone()
                datapair = (int(row[0]), float(row[1]))
                voltest_data.append(datapair)
            
            cur.execute("""SELECT  start_timestamp, speed from ie02 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowsspeed = int(cur.rowcount);
            for i in range(vnumrowsspeed):
                row = cur.fetchone()
                speedpair = (int(row[0]), float(row[1]))
                voltest_transferspeed.append(speedpair)
            
            
            cur.execute("""SELECT  start_timestamp, transfer_time from ie02 WHERE volume="voltest" and transfer_date>%s and transfer_date<%s ORDER BY start_timestamp""", (sdt,edt));
            vnumrowstime = int(cur.rowcount);
            for i in range(vnumrowstime):
                row = cur.fetchone()
                timepair = (int(row[0]), float(row[1])/60)
                voltest_transfertime.append(timepair)
            
        except mdb.Error,e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        
       
                
    #print len(transferspeed)    
    #print len(voltest_transferspeed)
    print "Select the graph to plot:"
    print "1) Only data"
    print "2) Only speed"
    print "3) Data + Speed combined"
    print "4) Data + Transfer Time  combined"
    
    
    
    
    choice = 0;
    while int(choice) not in [1,2,3,4]:
        choice = getchoice()
    
        
    if choice == "1":
        plotData(sitename, data, voltest_data,  svgout)
    elif choice == "2":
        plotSpeed(sitename, transferspeed, voltest_transferspeed, svgout)
    elif choice == "3":
        plotBoth(sitename, data, transferspeed, voltest_data, voltest_transferspeed, svgout)
    elif choice == "4":
        plotDataTime(sitename, data, transfertime, voltest_data, voltest_transfertime, svgout)
    else :
        print "Invalid choice"
        sys.exit(1)
        
            
if __name__ == '__main__':
    main()