from pydoc import Doc
import xml.etree.ElementTree as ET
import pandas as pd

def getPathNames(inXML, outPathNameCSV):
    tree = ET.parse(inXML)
    root = tree.getroot()

    Objects = root.iter('Object')

    pidDict = {}
    dfList = []

    # Iterate through every Reference, JobPlan, Plan, or Job object
    for obj in Objects:
        typeid = obj.get('typeid')
        if typeid in {'Reference', 'JobPlan', 'Plan', 'Job'}:
            ID = obj.findtext('ID')
            name = obj.findtext('Name')
            PID = obj.find('PID').findtext('ID')
            enabled = obj.findtext('Enabled')
            state = 'Enabled' if enabled == '1' else 'Disabled'
            description = obj.findtext('Description')
            doc = obj.find('Documentation').findtext('Documentation')
            pidDict.update({ID: [name, PID, state, typeid, description, doc]})

    # Create path name
    for id in pidDict:
        name = pidDict[id][0]
        pid = pidDict[id][1]
        state = pidDict[id][2]
        typeid = pidDict[id][3]
        desc = pidDict[id][4]
        doc = pidDict[id][5]
        pidName = pidDict[pid][0] if pid != '0' else 'SimCorp Dimension'
        pathName = ''
        tempPID = pid
        tempName = name

        # Generate the entire path name
        # Start at the lowest level and concatenate at the front 
        # until the highest level object is reached
        whileIdx = 0
        while True:
            pathName = tempName if whileIdx == 0 else tempName + '/' + pathName
            whileIdx += 1
            if tempPID == '0':
                break
            tempName = pidDict[tempPID][0]
            tempPID = pidDict[tempPID][1]
        
        dfList.append([id, name, pid, pidName, state, typeid, pathName, desc, doc])

    pathNameDict = pd.DataFrame(dfList, columns=['ID', 'NAME', 'PARENT_ID', 'PARENT_NAME', 'STATE', 'OBJECT_TYPE', 'PATH_NAME', 'DESCRIPTION', 'DOCUMENTATION'])
    pathNameDict = pathNameDict.set_index('ID')

    pathNameDict.to_csv(outPathNameCSV)

if __name__ == "__main__":
    getPathNames('XMLs\PROD_2022_10_12.xml', 'outputCSV\PathNames_PROD_20221012.csv')