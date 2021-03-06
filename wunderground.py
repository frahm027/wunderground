__author__ = 'Brett'


import urllib2
from BeautifulSoup import BeautifulSoup as BS
import time
import datetime
import xlwt
from Tkinter import *

def parseCurrentValues(name):
    url = "http://www.wunderground.com/cgi-bin/findweather/getForecast?query=pws:" + name
    content = urllib2.urlopen(url).read()
    html = BS(content)
    for times in html('div', {'class' : "local-time"}):
        LocalTime = times.find('span').text
    for current in html('span', {'data-variable' : 'dewpoint'}):
        if current.find('span', {'class' : 'wx-value'}):
            DewVal = current.find('span', {'class' : 'wx-value'}).text
        else:
            DewVal = "null"
    for current in html('div', {'id' : "current"}):
        if current.find('span', {'data-variable' : 'temperature'}):
            Temp = current.find('span', {'data-variable' : 'temperature'})
            TempVal = Temp.find('span', {'class' : 'wx-value'}).text
            TempUnit = Temp.find('span', {'class' : 'wx-unit'}).text
        else:
            TempVal = "null"
        if current.find('span', {'data-variable' : 'feelslike'}):
            HIndex = current.find('span', {'data-variable' : 'feelslike'})
            HIndexVal = HIndex.find('span', {'class' : 'wx-value'}).text
            HIndexUnit = HIndex.find('span', {'class' : 'wx-unit'}).text
        else:
            WchillVal = "null"
        if current.find('div', {'data-variable' : 'wind_speed'}):
            Wspeed = current.find('div', {'data-variable' : 'wind_speed'})
            WspeedVal = Wspeed.find('span', {'class' : 'wx-value'}).text
        else:
            WspeedVal = "null"
        if current.find('span', {'data-variable' : 'wind_gust_speed'}):
            WGspeed = current.find('span', {'data-variable' : 'wind_gust_speed'})
            WGspeedVal = WGspeed.find('span', {'class' : 'wx-value'}).text
            WGspeedUnit = WGspeed.find('span', {'class' : 'wx-unit'}).text
        else:
            WGspeedVal = "null"
        if current.find('span', {'data-variable' : 'pressure'}):
            Press = current.find('span', {'data-variable' : 'pressure'})
            PressVal = Press.find('span', {'class' : 'wx-value'}).text
            PressUnit = Press.find('span', {'class' : 'wx-unit'}).text
        else:
            PressVal = "null"
        if current.find('span', {'data-variable' : 'humidity'}):
            Humid = current.find('span', {'data-variable' : 'humidity'})
            HumidVal = Humid.find('span', {'class' : 'wx-value'}).text
            HumidUnit = Humid.find('span', {'class' : 'wx-unit'}).text
        else:
            HumidVal = "null"
        if current.find('span', {'data-variable' : 'precip_today'}):
            Precip = current.find('span', {'data-variable' : 'precip_today'})
            PrecipVal = Precip.find('span', {'class' : 'wx-value'}).text
            PrecipUnit = Precip.find('span', {'class' : 'wx-unit'}).text
        else:
            PrecipVal = "null"

    return name, LocalTime, TempVal, HIndexVal, DewVal, WspeedVal, WGspeedVal, PressVal, HumidVal, PrecipVal

def parseStationInfo(name):
    url = "http://www.wunderground.com/cgi-bin/findweather/getForecast?query=pws:" + name
    content = urllib2.urlopen(url).read()
    html = BS(content)
    for current in html('div', {'id' : "current"}):
        if current.find('span', {'data-variable' : 'station.elevation'}):
            Elev = current.find('span', {'data-variable' : 'station.elevation'})
            ElevVal = Elev.find('span', {'class' : 'wx-value'}).text
            ElevUnit = Elev.find('span', {'class' : 'wx-unit'}).text
        else:
            ElevVal = "null"
        if current.find('span', {'data-variable' : 'station.latitude'}):
            Lat = current.find('span', {'data-variable' : 'station.latitude'})
            LatVal = Lat.find('span', {'class' : 'wx-value'}).text
            LatUnit = Lat.find('span', {'class' : 'wx-unit'}).text
        else:
            LatVal = "null"
        if current.find('span', {'data-variable' : 'station.longitude'}):
            Long = current.find('span', {'data-variable' : 'station.longitude'})
            LongVal = Long.find('span', {'class' : 'wx-value'}).text
            LongUnit = Long.find('span', {'class' : 'wx-unit'}).text
        else:
            longVal = "null"

    return name, ElevVal, LatVal, LongVal


win = Tk()
fr = Frame(win).pack()
win.title("Weather Station HTML Parser")
stationVar = StringVar()
Label(fr, text="Station").pack()
station = Entry(fr, textvariable = stationVar).pack()
Label(fr, text="Interval").pack()
intervalVar = IntVar()
interval = Entry(fr, textvariable = intervalVar).pack()
lb = Listbox(fr, height=3)
stationList = []
ListCurrent = []
infoList = []


def insertStation():
    entry = stationVar.get()
    string = entry.split(" ")
    lb.insert(END, string[0])
    stationList.append(entry)


def delStation():
    selection = lb.get(ANCHOR)
    stationList.remove(selection)
    lb.delete(ANCHOR)


def startParser():
    intervalEntry = intervalVar.get()
    print intervalEntry
    print stationList
    startTime = datetime.datetime.now()
    print "start: {}"  .format(startTime)
    addTime = datetime.timedelta(seconds = 20)
    endTime = startTime
    print "end: {}"  .format(endTime)
    for i in range(0, intervalEntry):
        while datetime.datetime.now() < endTime:
            time.sleep(1)
            print datetime.datetime.now()
        else:
            for stations in stationList:
                print "station: " + stations
                for values in parseCurrentValues(stations):
                    ListCurrent.append(values)
                print ListCurrent
            i +=1
            endTime += addTime
            print "endTime2 = {}" .format(endTime)


def writeXL():
    workbook = xlwt.Workbook()
    FieldNames = ["Station", "Local Time", "Temp", "Heat_Index", "Dew_Point", "Wind_Speed", "Gust_Speed", "Pressure",
                    "Humidity", "Precip"]
    infoFieldNames = ["Station", "Elevation", "LatX", "LongY"]
    valuesheet = workbook.add_sheet('Values')
    infosheet = workbook.add_sheet('Info')

    col = 0
    col2 = 0
    for name in FieldNames:
        valuesheet.write(0,col,name)
        col +=1
    for item in enumerate(ListCurrent):
        item_str = str(item[0])
        column_number = int(item_str[-1])
        row_str = (item_str[:-1])
        if row_str == '':
            row_number = 1
        else:
            row_number = int(row_str)+1
        valuesheet.write(row_number, column_number, item[1])

    for name in infoFieldNames:
        infosheet.write(0, col2, name)
        col2 +=1
    dict = {key: [] for key in stationList}
    row = 1
    col3 = 0
    for station in stationList:
        for info in parseStationInfo(station):
            dict[station].append(info)
        for stuff in dict[station]:
            infosheet.write(row, col3, stuff)
            if col3 < 3:
                col3 +=1
            else:
                col3 = 0
        row +=1
    workbook.save('test.xls')


addBT = Button(fr, text = "Add", command = insertStation).pack()
delBT = Button(fr, text = "Delete", command = delStation).pack()
startBT = Button(fr, text = "Start", command = startParser).pack()
excelBT = Button(fr, text = "Write to Excel", command = writeXL).pack()
lb.pack()

sb = Scrollbar(fr, orient=VERTICAL)
sb.pack(side=RIGHT, fill = Y)
sb.configure(command=lb.yview)
lb.configure(yscrollcommand=sb.set)
win.mainloop()


