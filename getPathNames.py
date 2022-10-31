from pydoc import Doc
import xml.etree.ElementTree as ET
import pandas as pd

def getPathNames(xmlFile, outputCSVFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    Objects = root.iter('Object')

    pathNameDict = {}
    pathNameList = []

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
            pathNameDict.update({ID: [name, PID, state, typeid, description, doc]})

    # Create path name
    for id in pathNameDict:
        name = pathNameDict[id][0]
        pid = pathNameDict[id][1]
        state = pathNameDict[id][2]
        typeid = pathNameDict[id][3]
        desc = pathNameDict[id][4]
        doc = pathNameDict[id][5]
        pidName = pathNameDict[pid][0] if pid != '0' else 'SimCorp Dimension'
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
            tempName = pathNameDict[tempPID][0]
            tempPID = pathNameDict[tempPID][1]
        
        pathNameList.append([id, name, pid, pidName, state, typeid, pathName, desc, doc])

    # Output a CSV file from pathNameList using Pandas
    pathNameDict = pd.DataFrame(pathNameList, columns=['ID', 'NAME', 'PARENT_ID', 'PARENT_NAME', 'STATE', 'OBJECT_TYPE', 'PATH_NAME', 'DESCRIPTION', 'DOCUMENTATION'])
    pathNameDict = pathNameDict.set_index('ID')
    pathNameDict.to_csv(outputCSVFile)

if __name__ == "__main__":
    getPathNames('XMLs\PROD_2022_10_12.xml', 'outputCSV\PathNames_PROD_20221012.csv')