import xml.etree.ElementTree as ET
import pandas as pd
from createCSV import createCSV

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()

Objects = root.iter('Object')

pidDict = {}
pidList = []
lst = []

# Iterate through every Object element 
for obj in Objects:
    typeid = obj.get('typeid')
    if typeid in {'Reference', 'JobPlan', 'Plan', 'Job'}:
    # if  typeid == 'Reference' or typeid == 'JobPlan' or typeid == 'Plan' or typeid == 'Job':
        ID = obj.find('ID').text
        name = obj.find('Name').text
        PID = obj.find('PID').find('ID').text
        pidDict.update({ID: [name, PID, typeid]})

# Create path name
for id in pidDict:
    name = pidDict[id][0]
    pid = pidDict[id][1]
    typeid = pidDict[id][2]
    pidName = pidDict[pid][0] if pid != '0' else 'SimCorp Dimension'
    pathName = ''
    tempPID = pid
    tempName = name

    whileIdx = 0
    while True:
        pathName = tempName if whileIdx == 0 else tempName + '/' + pathName
        whileIdx += 1
        if tempPID == '0':
            break
        tempName = pidDict[tempPID][0]
        tempPID = pidDict[tempPID][1]
    lst.append([id, name, pid, pidName, typeid, pathName])

pathNameDF = pd.DataFrame(lst, columns=['ID', 'Name', 'Parent ID', 'Parent Name', 'Object Type', 'Path Name'])
pathNameDF.to_csv('outputCSV/Path_Names.csv', index=False)

# Create a list of all Job Plans as dictionaries
# pidColumns = ['ID', 'Name', 'PID', 'Type ID', 'Path Name']

# createCSV(pidList, pidDict, pidColumns, 'outputCSV\Path_Names_test.csv')