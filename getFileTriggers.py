import xml.etree.ElementTree as ET
import pandas as pd

def getFileTriggers(inXML, inVariablesCSV, outCSV):
    tree = ET.parse(inXML)
    root = tree.getroot()
    Events = root.iter('Event')

    fileTriggerList = []
    variablesDF = pd.read_csv(inVariablesCSV, index_col='ID')

    # Iterate through every Event element 
    for event in Events:
        typeid = event.get('typeid')
        if typeid == 'Event':
            label = event.find('ID').findtext('Label')
            if 'FileTrigger' not in label:
                continue

            ID = event.find('ID').findtext('ID')
            enabledFlag = 'True' if event.findtext('Enabled') == '1' else 'False'
            PIDName = event.find('PID').findtext('ID')

            description = ''

            for var in event.find('Properties').findall('Variable'):
                if var.findtext('Name') != 'Filter':
                    continue
                description = var.findtext('Value')

            fileTriggerList.append([ID, label, enabledFlag, PIDName, description])

    fileTriggerColumns = ['EVENT_ID', 'TRIGGERED_LABEL', 'ENABLED?', 'TRIGGER_PLAN', 'FILE_DESCRIPTION']
    fileTriggerDF = pd.DataFrame(fileTriggerList, columns=fileTriggerColumns)
    fileTriggerDF = fileTriggerDF.set_index('EVENT_ID')

    fileTriggerDF.to_csv(outCSV)

if __name__ == '__main__':
    getFileTriggers('XMLs\PROD_20221004.xml', 'outputCSV\FileTriggers_PROD_test.csv')