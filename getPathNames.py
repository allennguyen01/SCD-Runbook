import xml.etree.ElementTree as ET
import csv
from createCSV import createCSV

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()

Objects = root.iter('Object')

pidDict = {}
pidList = []

# Iterate through every Object element 
for obj in Objects:
    typeid = obj.get('typeid')
    if  typeid == 'Reference' or typeid == 'JobPlan' or typeid == 'Plan':
        ID = obj.find('ID').text
        name = obj.find('Name').text
        PID = obj.find('PID').find('ID').text
        pidDict.update({ID: [name, PID, typeid]})

# Create path name
for id in pidDict:
    name = pidDict[id][0]
    pid = pidDict[id][1]
    typeid = pidDict[id][2]
    pathName = ''
    tempPID = pid
    tempName = name
    while True:
        pathName = tempName + '/' + pathName
        if tempPID == '0':
            break
        tempName = pidDict[tempPID][0]
        tempPID = pidDict[tempPID][1]
    pidDict.update({id : [name, pid, typeid, pathName]})

# trn_fit_id = '15101196'
# print(pidDict[trn_fit_id][0], pidDict[trn_fit_id][(len(pidDict[trn_fit_id])-1)])

# Create a list of all Job Plans as dictionaries
pidColumns = ['ID', 'Name', 'PID', 'Type ID', 'Path Name']

createCSV(pidList, pidDict, pidColumns, 'outputCSV\Path_Names_test.csv')