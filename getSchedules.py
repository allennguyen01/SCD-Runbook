import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()

Objects = root.iter('Object')

scheduleDict = {}
scheduleList = []

# Iterate through every Object element 
for obj in Objects:
    if obj.get('typeid') == 'Schedule':
        ID = obj.find('ID').text
        name = obj.find('Name').text
        scheduleDict.update({ID : name})

scheduleDF = pd.DataFrame(scheduleDict.items(), columns=['ID', 'Schedule Name'])
scheduleDF = scheduleDF.set_index('ID')

scheduleDF.to_csv('outputCSV/Schedules.csv')