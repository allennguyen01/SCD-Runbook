import xml.etree.ElementTree as ET
import pandas as pd
from getPathNames import pathNameDF 

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()

Events = root.iter('Event')

eventsDict = {}
eventsList = []

triggerDictionary = {'2' : 'Alert Trigger: Job/Plan Completed', '4' : 'Failed Completion Trigger', '5' : 'Success Completion Trigger'}

for event in Events:
    typeid = event.get('typeid')
    if typeid == 'Event':
        ID = event.find('Actions').find('EventAction').find('CommandArgument').find('ID')
        ID = ID.text if ID is not None else ''
        if ID == '':
            continue
        name = pathNameDF.loc[ID]['Name']

        label = event.find('ID').find('Label').text
        if 'FileTrigger' in label:
            continue
        # eventID = event.find('EventID').text
        v4Tag = event.find('V4Tag').text
        label = triggerDictionary[v4Tag] if v4Tag in triggerDictionary else ''
        parentID = event.find('PID').find('ID').text
        parentName = event.find('PID').find('Name').text
        
        eventsList.append([ID, name, parentName, parentID, label])
        eventsDict.update({ID : [name, parentName, parentID]})

for id in eventsDict:
    currParentID = eventsDict[id][2]
    if currParentID not in eventsDict:
        # Add first job that executes
        ID = currParentID
        try:
            currObj = pathNameDF.loc[ID]
        except:
            continue
        name = currObj['Name']
        parentName = currObj['Parent Name']
        parentID = currObj['Parent ID']
        label = 'First Batch Job Group'
        eventsList.append([ID, name, parentName, parentID, label])

        # Add top level plan
        ID = parentID
        currObj = pathNameDF.loc[ID]
        name = currObj['Path Name']
        parentName = currObj['Parent Name']
        parentID = currObj['Parent ID']
        label = 'Top-level Plan'
        eventsList.append([ID, name, parentName, parentID, label])

eoDF = pd.DataFrame(eventsList, columns=['ID', 'Name', 'Parent Name', 'Parent ID', 'Label'])
eoDF = eoDF.set_index('ID')

eoDF.to_csv('outputCSV\ExecutionOrder_test_1.csv')
