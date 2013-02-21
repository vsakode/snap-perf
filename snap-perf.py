#!/usr/bin/python
'''
Created on Nov 22, 2011

@author: Vikas Sakode
'''

import re;
import commands;
import os;
import datetime;
import time;
import sys;
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
def main():
    start_flag=0
    sche_ts=0
    if len(sys.argv) < 2:
        pass
        usage()
    
    try:
        filename = sys.argv[1]
        token = open(filename,'rU')
        yr1 = checkyear(filename)
        outfile = filename + "." + str(int(time.time()))
        dataout = outfile + ".data"
        os.chdir('output/data')
        fout = open(dataout,'w')
        svgout = outfile + ".svg"
    except :
        print 'Unable to open', filename
    else:
        data = []
        transferspeed = []
        
        for line in token:
            requested = None
            started = None
            ended = None
            requested = re.search('Scheduled', line)
            started = re.search('Start',line)
            ended = re.search('End',line)
            
            if requested:
                sline = line.split()
                timestr = sline[1] + ' ' +sline[2] + ' ' +sline[3] + ' ' +sline[4] + ' ' +sline[5] + ' ' + yr1
                time_tup = time.strptime(timestr, "%a %b %d %H:%M:%S %Z %Y")
                sche_ts = int(time.mktime(time_tup))
            if started:
                if sche_ts == 0 :
                    pass
                else: 
                    #print 'started successfully'
                    start_flag=1;
            
            if ended:
                if start_flag == 1 and sche_ts:
                    sline = line.split()
                    timestr = sline[1] + ' ' +sline[2] + ' ' +sline[3] + ' ' +sline[4] + ' ' +sline[5] + ' ' +yr1
                    data_transfered= sline[9]
                    transferedData = data_transfered[1:]
                    time_tup = time.strptime(timestr, "%a %b %d %H:%M:%S %Z %Y")
                    end_ts = int(time.mktime(time_tup))
                    time_taken = int(end_ts) - int(sche_ts)
                    
                    speed = int(transferedData) / int(time_taken)
                    gbdata = float (transferedData) / 1024 /1024
                    
                    datapair = (int(sche_ts), int(gbdata))
                    speedpair = (int(sche_ts), int(speed))
                    
                    data.append(datapair)
                    transferspeed.append(speedpair)
                    
                    print >> fout,time.ctime(int(sche_ts)),'\t', gbdata
            
                    start_flag = 0
                    sche_ts = 0
                else:
                    pass
        os.chdir('../graphs')            
        can = canvas.init(svgout)
        size = (3600, 800)
        ar = area.T(legend=legend.T(loc=(3650,100)),size = size,
                    x_coord= category_coord.T(data,0),
                    y_grid_interval=2,
                    x_axis = axis.X(format=format_date, label="Date"),
         	        y_axis = axis.Y(label="Data Transfered ( GB )"))
        ar.add_plot(bar_plot.T(label="Data",data=data))
        ar.draw()
        can.set_author("Vikas Sakode")
        ar.draw(can)
        tb = text_box.T(fill_style=fill_style.gray90,loc=(1600,820),text="SnapMirror Performance", line_style=None)
        tb.draw(can)
        ar = area.T(legend=legend.T(loc=(3650,120)), size=size,
                    x_coord= category_coord.T(transferspeed,0),
                    x_axis = None, 
                    #y_grid_interval=500,
                    y_axis2 = axis.Y(offset=3600, label = "Transfer Speed (kb//sec)", draw_tics_right=1))
                    #y_axis = axis.Y(offset=300,
                    #                label_offset=(10, 0), label="Speed"))
        ar.add_plot(line_plot.T(line_style=line_style.blue, label="Speed",data=transferspeed, tick_mark=tick_mark.x3))
        ar.draw()
        

        fout.close()
        print 'Script completed successfully'
        print '[INFO] Data file ' + dataout + ' is created in output/data directory'
        print '[INFO] SVG Graph file ' + svgout + ' is created in output/graphs directory.'
        print '       Best viewed in CHROME Browser'

if __name__ == '__main__':
    main()
