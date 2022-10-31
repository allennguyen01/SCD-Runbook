import xml.etree.ElementTree as ET
import pandas as pd
from datetime import *

# Gets the Time Specification from ActiveBatch XML as HH:MM:SS format
def getTime(obj):
    try:
        timeText = obj.findall('./Properties/Variable')[1].findall('./Value/Variable/Value/Variable')[2].findtext('Value')
    except IndexError:
        print(IndexError, 'Scheduled Time Not Found', obj.findtext('Name'))
        return

    # timeText = obj.findtext('[[.="ExactTimes"]="Value"]/../Value')

    # Get time in HH:MM:SS format as time object 
    timeHMS = timeText.split('T')[1].split(':')
    tHour, tMin, tSec = map(int, timeHMS)
    t = time(tHour, tMin, tSec)
    
    return t

# TODO: Find ActiveBatch Day Specifications and add them to scheduleDF (WEEKDAY, EOM, etc.)
# BUG: Some Time Specifications are not being added (e.g. SCD_DAILY_1am, SCD_EOM_1145pm)
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
            # timeText = obj.findtext('[[.="ExactTimes"]="Value"]/../Value')
            # timeText = obj.findtext('//Name[.="ExactTimes"]')
            # timeText = obj.findtext("ID[.='15104839']")
            # print(ID, name, timeText)

            schTime = getTime(obj)
            scheduleList.append([ID, name, schTime])

    scheduleColumns = ['ID', 'SCHEDULE_NAME', 'TIME']
    scheduleDF = pd.DataFrame(scheduleList, columns=scheduleColumns)
    scheduleDF = scheduleDF.set_index('ID')
    scheduleDF.to_csv(outputCSVFile)

if __name__ == "__main__":
    getSchedules('XMLs\PROD_20221004.xml','outputCSV/Schedules_prod_1.csv')