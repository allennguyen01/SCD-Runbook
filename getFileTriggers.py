import xml.etree.ElementTree as ET
from createCSV import createCSV

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()

Events = root.iter('Event')

eventsDict = {}
eventsList = []
eventColumns = ['ID', 'Trigger Label', 'Enabled Flag', 'Triggered Plan', 'Description']

# Iterate through every Event element 
for event in Events:
    typeid = event.get('typeid')
    if typeid == 'Event':
        # Store FileTriggers in dictionary with {ID : [Name, EnabledFlag, TriggeredPlanName, FileDescription]}
        label = event.find('ID').find('Label').text
        if 'FileTrigger' not in label:
            continue

        ID = event.find('ID').find('ID').text
        
        enabledFlag = event.find('Enabled').text
        PIDName = event.find('PID').find('Name').text

        description = ''
        for var in event.find('Properties').findall('Variable'):
            varName = var.find('Name').text
            if varName != 'Filter':
                continue
            description = var.find('Value').text

        eventsDict.update({ID : [label, enabledFlag, PIDName, description]})

createCSV(eventsList, eventsDict, eventColumns, 'outputCSV\Events.csv')