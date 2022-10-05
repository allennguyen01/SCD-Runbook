import xml.etree.ElementTree as ET
import pandas as pd

def getExecutionOrder(inXML, inPathNameCSV, outExecutionOrderCSV):
    tree = ET.parse(inXML)
    root = tree.getroot()

    Events = root.iter('Event')

    eventsDict = {}
    eventsList = []
    pathNameDict = pd.read_csv(inPathNameCSV, index_col='ID')

    triggerDictionary = {'2' : 'Alert Trigger: Job/Plan Completed', '4' : 'Failed Completion Trigger', '5' : 'Success Completion Trigger'}

    for event in Events:
        typeid = event.get('typeid')
        if typeid == 'Event':
            ID = event.find('Actions').find('EventAction').find('CommandArgument').find('ID')
            ID = ID.text if ID is not None else ''
            if ID == '':
                continue
            name = pathNameDict.loc[int(ID)]['Name']

            label = event.find('ID').find('Label').text
            if 'FileTrigger' in label:
                continue

            v4Tag = event.find('V4Tag').text
            label = triggerDictionary[v4Tag] if v4Tag in triggerDictionary else None
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
                currObj = pathNameDict.loc[int(ID)]
            except:
                continue
            name = currObj['Name']
            parentName = currObj['Parent Name']
            parentID = currObj['Parent ID']
            label = 'Starting Plan'
            eventsList.append([ID, name, parentName, parentID, label])

            # Add top level plan
            ID = parentID
            currObj = pathNameDict.loc[int(ID)]
            name = currObj['Path Name']
            parentName = currObj['Parent Name']
            parentID = currObj['Parent ID']
            label = 'Top-Level Plan'
            eventsList.append([ID, name, parentName, parentID, label])

    eoDF = pd.DataFrame(eventsList, columns=['ID', 'Name', 'Parent Name', 'Parent ID', 'Label'])
    eoDF = eoDF.set_index('ID')
    eoDF = eoDF.drop_duplicates(keep='first')

    eoDF.to_csv(outExecutionOrderCSV)

if __name__ == '__main__':
    getExecutionOrder('XMLs\PROD_20221004.xml', 'outputCSV\PathNames_PROD.csv', 'outputCSV\ExecutionOrder_PROD.csv')