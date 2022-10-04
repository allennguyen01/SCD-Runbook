import xml.etree.ElementTree as ET
import pandas as pd
from datetime import *

tree = ET.parse('XMLs\SCHEDULES_PROD.xml')
root = tree.getroot()

Objects = root.iter('Object')

scheduleDict = {}
scheduleList = []

def getTime(obj):
    try:
        timeText = obj.findall('./Properties/Variable')[1].findall('./Value/Variable/Value/Variable')[2].findtext('Value')
    except IndexError:
        print(IndexError, obj.find('Name').text)
        return

    # timeText = obj.findtext('[[.="ExactTimes"]="Value"]/../Value')

    timeHMS = timeText.split('T')[1].split(':')
    tHour, tMin, tSec = map(int, timeHMS)
    t = time(tHour, tMin, tSec)
    
    return t

# Iterate through every Object element 
for obj in Objects:
    if obj.get('typeid') == 'Schedule':
        ID = obj.findtext('ID')
        name = obj.findtext('Name')
        # timeText = obj.findtext('[[.="ExactTimes"]="Value"]/../Value')
        # timeText = obj.findtext('//Name[.="ExactTimes"]')
        # timeText = obj.findtext("ID[.='15104839']")
        # print(ID, name, timeText)

        schTime = getTime(obj)
        scheduleList.append([ID, name, schTime])

scheduleDF = pd.DataFrame(scheduleList, columns=['ID', 'Schedule Name', 'Time'])
print(scheduleDF)
scheduleDF = scheduleDF.set_index('ID')

# scheduleDF.to_csv('outputCSV/Schedules_prod.csv')

