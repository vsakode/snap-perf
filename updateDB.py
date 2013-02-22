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
    if mline[6] != "2012":
        print "Missing year in date timestamp"
        nyear = getyear()
    return nyear

def getSite(nfile):
    sitetoken = "head -1 " + nfile + "| awk '{print $8}' | cut -d '-' -f 1"
    token = commands.getoutput(sitetoken)
    return token
         
        
def getyear():
    print "Enter the year (YYYY)[Default : 2012] :"
    nyear = raw_input()
    if not nyear:
        year = "2012"
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
    voltest_start_flag=0
    voltest_sche_ts=0
    if len(sys.argv) < 2:
        pass
        usage()
    
    try:
        scriptdir = os.getcwd()
        filename = sys.argv[1]
        dir = os.path.dirname(filename)
        file = os.path.basename(filename)
        #print dir
        #print file
        if not dir:
            os.chdir(scriptdir)
        else: 
            os.chdir(dir)
        token = open(file,'rU')
        #yr1 = checkyear(file)
	yr1 = "2012"
        sitename = getSite(file)
        outfile = file + "." + str(int(time.time()))
        dataout = outfile + ".data"
        os.chdir(scriptdir)
        os.chdir('output/data')
        fout = open(dataout,'w')
    except :
        print 'Unable to open', filename
        print "Check the Permissions"
    else:
        data = []
        transferspeed = []
        entries = []
       
        for line in token:
            vol = None
            vol = re.search('voltest',line)
            
            if vol:
                started = None
                ended = None
                volstart = None
                started = re.search('Start',line)
                ended = re.search('End',line)
                volstart = re.search('Request', line )
                if volstart:
                    sline = line.split()
                    timestr = sline[1] + ' ' +sline[2] + ' ' +sline[3] + ' ' +sline[4] + ' ' +sline[5] + ' ' + yr1
                    #print timestr
                    time_tup = time.strptime(timestr, "%a %b %d %H:%M:%S %Z %Y")
                    mon = time_tup.__getattribute__('tm_mon')
                    day = time_tup.__getattribute__('tm_mday')
                    date_field = str(yr1) + '-' + str(mon) + '-' + str(day)
                    voltest_sche_ts = int(time.mktime(time_tup))
                if started:
                    if voltest_sche_ts == 0 :
                        pass
                    else: 
                        #print 'started successfully'
                        voltest_start_flag=1;
                
                if ended:
                    if voltest_start_flag == 1 and voltest_sche_ts:
                        sline = line.split()
                        timestr = sline[1] + ' ' +sline[2] + ' ' +sline[3] + ' ' +sline[4] + ' ' +sline[5] + ' ' +yr1
                        data_transfered = sline[9]
                        transferedData = data_transfered[1:]
                        time_tup = time.strptime(timestr, "%a %b %d %H:%M:%S %Z %Y")
                        end_ts = int(time.mktime(time_tup))
                        time_taken = int(end_ts) - int(voltest_sche_ts)
                        
                        speed = float(transferedData) / int(time_taken) / 1024 * 8
                        gbdata = float (transferedData) / 1024 / 1024
                      
                        entry = (int(voltest_sche_ts),date_field,"voltest", gbdata, speed, time_taken)
                        entries.append(entry)
                        
                        datapair = (int(voltest_sche_ts), int(gbdata))
                        speedpair = (float(voltest_sche_ts), int(speed))
                        
                        data.append(datapair)
                        transferspeed.append(speedpair)
                        
                        print >> fout,time.ctime(int(voltest_sche_ts)),'\t', gbdata, '\t', speed, '\t', time_taken 
                
                        voltest_start_flag = 0
                        voltest_sche_ts = 0
                    else:
                        pass
            else:
                requested = None
                started = None
                ended = None
                requested = re.search('Scheduled', line)
                started = re.search('Start',line)
                ended = re.search('End',line)
                if requested:
                    sline = line.split()
                    timestr = sline[1] + ' ' +sline[2] + ' ' +sline[3] + ' ' +sline[4] + ' ' +sline[5] + ' ' + yr1
                    #print timestr
                    time_tup = time.strptime(timestr, "%a %b %d %H:%M:%S %Z %Y")
                    mon = time_tup.__getattribute__('tm_mon')
                    day = time_tup.__getattribute__('tm_mday')
                    date_field = str(yr1) + '-' + str(mon) + '-' + str(day)
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
                        data_transfered = sline[9]
                        transferedData = data_transfered[1:]
                        time_tup = time.strptime(timestr, "%a %b %d %H:%M:%S %Z %Y")
                        end_ts = int(time.mktime(time_tup))
                        time_taken = int(end_ts) - int(sche_ts)
                        
                        speed = float(transferedData) / int(time_taken) / 1024 * 8
                        gbdata = float (transferedData) / 1024 / 1024
                      
                        entry = (int(sche_ts),date_field, "vol1", gbdata, speed, time_taken)
                        entries.append(entry)
                        
                        datapair = (int(sche_ts), int(gbdata))
                        speedpair = (float(sche_ts), int(speed))
                        
                        data.append(datapair)
                        transferspeed.append(speedpair)
                        
                        print >> fout,time.ctime(int(sche_ts)),'\t', gbdata, '\t', speed, '\t', time_taken 
                
                        start_flag = 0
                        sche_ts = 0
                    else:
                        pass
                    
                    
        
        con = None
        try:
            con = mdb.connect('dbhost', 'dbuser', 'dbpasswd', 'dbname')
            cur = con.cursor()
            #print sitename
            #print sitename
            if sitename == "hu01":
                #print "hu01"
                cur.execute("CREATE TABLE IF NOT EXISTS hu01 (start_timestamp BIGINT PRIMARY KEY, transfer_date DATE, volume VARCHAR(10), data_transfered DOUBLE, speed FLOAT, transfer_time INT )");
                cur.executemany("""INSERT IGNORE INTO hu01 (start_timestamp,transfer_date, volume, data_transfered, speed,transfer_time) VALUES (%s,%s,%s,%s,%s,%s)""", entries)
            elif sitename == "us01":
                #print "us01"
                cur.execute("CREATE TABLE IF NOT EXISTS us01 (start_timestamp BIGINT PRIMARY KEY, transfer_date DATE, volume VARCHAR(10), data_transfered DOUBLE, speed FLOAT, transfer_time INT )");
                cur.executemany("""INSERT IGNORE INTO us01 (start_timestamp,transfer_date,volume, data_transfered, speed,transfer_time) VALUES (%s,%s,%s,%s,%s,%s)""", entries)
            elif sitename == "de02":
                #print "de02"
                cur.execute("CREATE TABLE IF NOT EXISTS de02 (start_timestamp BIGINT PRIMARY KEY, transfer_date DATE, volume VARCHAR(10), data_transfered DOUBLE, speed FLOAT, transfer_time INT )");
                cur.executemany("""INSERT IGNORE INTO de02 (start_timestamp,transfer_date,volume, data_transfered, speed,transfer_time) VALUES (%s,%s,%s,%s,%s,%s)""", entries)
            elif sitename == "ie02":
                #print "ie02"
                cur.execute("CREATE TABLE IF NOT EXISTS ie02 (start_timestamp BIGINT PRIMARY KEY, transfer_date DATE, volume VARCHAR(10), data_transfered DOUBLE, speed FLOAT, transfer_time INT )");
                cur.executemany("""INSERT IGNORE INTO ie02 (start_timestamp,transfer_date,volume ,data_transfered, speed,transfer_time) VALUES (%s,%s,%s,%s,%s,%s)""", entries)
            print "Database Updated Successfully"
        except mdb.Error,e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        
        if con:
            con.close
            
if __name__ == '__main__':
    main()
