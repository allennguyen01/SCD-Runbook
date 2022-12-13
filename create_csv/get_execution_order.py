import xml.etree.ElementTree as ET
import pandas as pd

# TODO: Add the top level plan for execution order 
def get_execution_order(xmlFile, pathnameCSVFile, outputCSVFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    Events = root.iter('Event')

    eventsDict = {}
    eoList = []
    pathNameDict = pd.read_csv(pathnameCSVFile, index_col='ID')

    triggerDictionary = {'2' : 'Alert Trigger: Job/Plan Completed', '4' : 'Failed Completion Trigger', '5' : 'Success Completion Trigger'}

    # Iterate through every Event object with typeid 'Event'
    for event in Events:
        typeid = event.get('typeid')
        if typeid == 'Event':
            ID = event.find('./Actions/EventAction/CommandArgument/ID')
            ID = ID.text if ID is not None else ''
            if ID == '':
                continue
            name = pathNameDict.loc[int(ID)]['NAME']

            label = event.findtext('./ID/Label')
            if 'FileTrigger' in label:
                continue

            v4Tag = event.findtext('V4Tag')
            label = triggerDictionary[v4Tag] if v4Tag in triggerDictionary else None
            parentID = event.findtext('./PID/ID')
            parentName = event.findtext('./PID/Name')
            
            eoList.append([ID, name, parentName, parentID, label])
            eventsDict.update({ID : [name, parentName, parentID]})

    # Get starting plan and top-level plan from ActiveBatch map view
    for id in eventsDict:
        currParentID = eventsDict[id][2]
        if currParentID not in eventsDict:
            # Add starting plan that executes first
            ID = currParentID
            try:
                currObj = pathNameDict.loc[int(ID)]
            except KeyError:
                print(f'{KeyError}, ID key ({ID}) not found')
                continue
            name = currObj['NAME']
            parentName = currObj['PARENT_NAME']
            parentID = currObj['PARENT_ID']
            label = 'Starting Plan'
            eoList.append([ID, name, parentName, parentID, label])

            # Add top level plan that executes starting plan
            ID = parentID
            currObj = pathNameDict.loc[int(ID)]
            name = currObj['PATH_NAME']
            parentName = currObj['PARENT_NAME']
            parentID = currObj['PARENT_ID']
            label = 'Top-Level Plan'
            eoList.append([ID, name, parentName, parentID, label])

    # Output a CSV file with Pandas using eoList and drop any duplicate rows
    eoColumns = ['ID', 'Name', 'Parent Name', 'Parent ID', 'Label']
    eoDF = pd.DataFrame(eoList, columns=eoColumns)
    eoDF = eoDF.set_index('ID')
    eoDF = eoDF.drop_duplicates(keep='first')
    eoDF.to_csv(outputCSVFile)

if __name__ == '__main__':
    get_execution_order('XMLs\PROD_20221004.xml', 'outputCSV\PathNames_PROD.csv', 'outputCSV\ExecutionOrder_PROD_1.csv')