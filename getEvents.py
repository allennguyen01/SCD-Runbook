from cgitb import enable
import xml.etree.ElementTree as ET
from createCSV import createCSV

tree = ET.parse('XMLs\TRN_FUT_TRIGGERED_DISABLED.xml')
root = tree.getroot()

Events = root.iter('Event')

eventsDict = {}
eventsList = []
eventColumns = ['ID', 'Label', 'Enabled Flag', 'PID Name']

# Iterate through every Event element 
for event in Events:
    if event.get('typeid') == 'Event':
        # Store Events in dictionary with {ID : [name, enabledFlag, PIDName]}
        ID = event.find('ID').find('ID').text
        label = event.find('ID').find('Label').text
        enabledFlag = event.find('Enabled').text
        PIDName = event.find('PID').find('Name').text
        eventsDict.update({ID : [label, enabledFlag, PIDName]})

createCSV(eventsList, eventsDict, eventColumns, 'outputCSV\Events_Disabled_TRN_FUT.csv')