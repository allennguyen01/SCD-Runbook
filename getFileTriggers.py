import xml.etree.ElementTree as ET
import pandas as pd

def getFileTriggers(xmlFile, outputCSVFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    Events = root.iter('Event')

    fileTriggerList = []

    # Iterate through every Event object and find labels with 'FileTrigger'
    for event in Events:
        typeid = event.get('typeid')
        if typeid == 'Event':
            label = event.find('ID').findtext('Label')
            if 'FileTrigger' not in label:
                continue

            ID = event.find('ID').findtext('ID')
            enabledFlag = 'True' if event.findtext('Enabled') == '1' else 'False'
            PIDName = event.find('PID').findtext('ID')

            # Iterate through every Variable object and find the file description
            description = ''
            for var in event.find('Properties').findall('Variable'):
                if var.findtext('Name') != 'Filter':
                    continue
                description = var.findtext('Value')

            fileTriggerList.append([ID, label, enabledFlag, PIDName, description])

    # Output a CSV file with Pandas using fileTriggerList
    fileTriggerColumns = ['EVENT_ID', 'TRIGGERED_LABEL', 'ENABLED?', 'TRIGGER_PLAN', 'FILE_DESCRIPTION']
    fileTriggerDF = pd.DataFrame(fileTriggerList, columns=fileTriggerColumns)
    fileTriggerDF = fileTriggerDF.set_index('EVENT_ID')
    fileTriggerDF.to_csv(outputCSVFile)

if __name__ == '__main__':
    getFileTriggers('XMLs\PROD_20221004.xml', 'outputCSV\FileTriggers_PROD_test_1.csv')