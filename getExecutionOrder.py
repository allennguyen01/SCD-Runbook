import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('XMLs\SCD_DWH_LOAD.xml')
root = tree.getroot()

Events = root.iter('Event')

eventsDict = {}
eventsList = []

# Iterate through every Event element 
for event in Events:
    typeid = event.get('typeid')
    if typeid == 'Event':
        label = event.find('ID').find('Label').text
        if 'FileTrigger' in label:
            continue
        ID = event.find('PID').find('ID').text
        pidName = event.find('PID').find('Name').text
        nextActionID = event.find('Actions').find('EventAction').find('CommandArgument').find('ID')
        nextActionID = nextActionID.text if nextActionID is not None else ''
        eventsList.append([ID, label, pidName, nextActionID])

actionsDF = pd.DataFrame(eventsList, columns=['ID', 'Action Label', 'Parent Name', 'Next Action ID'])
actionsDF.to_csv('outputCSV\ExecutionOrder.csv', index=False)
