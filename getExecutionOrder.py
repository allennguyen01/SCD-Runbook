import xml.etree.ElementTree as ET
import pandas as pd
from getPathNames import pathNameDF 

tree = ET.parse('XMLs\SCD_DWH_LOAD.xml')
root = tree.getroot()

Events = root.iter('Event')

eventsDict = {}
eventsList = []

# Iterate through every Event element 
# for event in Events:
#     typeid = event.get('typeid')
#     if typeid == 'Event':
#         label = event.find('ID').find('Label').text
#         if 'FileTrigger' in label:
#             continue
#         ID = event.find('PID').find('ID').text
#         pidName = event.find('PID').find('Name').text
#         nextActionID = event.find('Actions').find('EventAction').find('CommandArgument').find('ID')
#         nextActionID = nextActionID.text if nextActionID is not None else ''
#         eventsList.append([ID, label, pidName, nextActionID])

for event in Events:
    typeid = event.get('typeid')
    if typeid == 'Event':
        ID = event.find('Actions').find('EventAction').find('CommandArgument').find('ID')
        ID = ID.text if ID is not None else ''
        name = pathNameDF.loc[ID]['Name']

        label = event.find('ID').find('Label').text
        if 'FileTrigger' in label:
            continue
        parentID = event.find('PID').find('ID').text
        parentName = event.find('PID').find('Name').text
        
        eventsList.append([ID, name, parentName, parentID])
        eventsDict.update({ID : [name, parentName, parentID]})

for id in eventsDict:
    currParentID = eventsDict[id][2]
    if currParentID not in eventsDict:
        # Add first job that executes
        ID = currParentID
        currObj = pathNameDF.loc[ID]
        name = currObj['Name']
        parentName = currObj['Parent Name']
        parentID = currObj['Parent ID']
        eventsList.append([ID, name, parentName, parentID])

        # Add top level plan
        ID = parentID
        currObj = pathNameDF.loc[ID]
        name = currObj['Path Name']
        parentName = currObj['Parent Name']
        parentID = None
        eventsList.append([ID, name, parentName, parentID])

eoDF = pd.DataFrame(eventsList, columns=['ID', 'Name', 'Parent Name', 'Parent ID'])
eoDF = eoDF.set_index('ID')

eoDF.to_csv('outputCSV\ExecutionOrder_SCD_DWH_LOAD.csv')
