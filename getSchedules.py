import xml.etree.ElementTree as ET
import pandas as pd
from datetime import time

# Gets the Time Specification from ActiveBatch XML as HH:MM:SS format
def getTime(obj):
    name = obj.findtext('Name')
    try:
        timeText = obj.find(".//*[.='ExactTimes']../Value/Variable/Value/.//*[.='Value']../Value").text
    except AttributeError:
        print(f'{AttributeError}, Time Specification not provided for {name}')
        return

    # Get time in HH:MM:SS format as time object 
    timeHMS = timeText.split('T')[1].split(':')
    tHour, tMin, tSec = map(int, timeHMS)
    t = time(tHour, tMin, tSec)
    
    return t

# TODO: Find ActiveBatch Day Specifications and add them to scheduleDF (WEEKDAY, EOM, etc.)
def getSchedules(xmlFile, outputCSVFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    Objects = root.iter('Object')

    scheduleList = []

    # Iterate through every Object element with typeid 'Schedule'
    for obj in Objects:
        if obj.get('typeid') == 'Schedule':
            ID = obj.findtext('ID')
            name = obj.findtext('Name')
            if name == '$Schedule':
                continue
            schTime = getTime(obj)
            scheduleList.append([ID, name, schTime])

    # Output a CSV file from schedulesList using Pandas
    scheduleColumns = ['ID', 'ScheduleName', 'Times']
    scheduleDF = pd.DataFrame(scheduleList, columns=scheduleColumns)
    scheduleDF = scheduleDF.set_index('ID')
    scheduleDF.to_csv(outputCSVFile)

if __name__ == "__main__":
    getSchedules('XMLs\PROD_20221004.xml','outputCSV/Schedules_PROD.csv')