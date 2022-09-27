import xml.etree.ElementTree as ET
import pandas as pd
from getPathNames import pidDict 

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
        name = pidDict[ID][0]

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
        ID = currParentID
        name = pidDict[ID][0]
        parentID = pidDict[ID][1]
        parentPathName = pidDict[ID][4]
        eventsList.append(ID, name, parentPathName, parentID)


eoDF = pd.DataFrame(eventsList, columns=['ID', 'Name', 'Parent Name', 'Parent ID'])
eoDF.to_csv('outputCSV\ExecutionOrder_SCD_DWH_LOAD_1.csv', index=False)
