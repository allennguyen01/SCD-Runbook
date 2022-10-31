import xml.etree.ElementTree as ET
import csv
import pandas as pd
# from getJobPlans import jobPlanDict

def getBatchJobGroups(xmlFile, pathnameCSVFile, outputCSVFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    pathNameDF = pd.read_csv(pathnameCSVFile, index_col='ID')

    Objects = root.iter('Object')
    batchJobGroupList = []

    # Iterate through every Object element 
    for obj in Objects:
        # If object is of Reference type, get the data of the object
        if obj.get('typeid') == 'Reference':
            name = obj.findtext('Name')
            ID = obj.findtext('ID')
            PID = obj.findtext('./PID/ID')
            parentObj = pathNameDF.loc[int(PID)]
            if parentObj['OBJECT_TYPE'] != 'JobPlan':
                continue
            PIDName = pathNameDF.loc[int(PID)]['NAME']
            batchJobGroupList.append([ID, name, PID, PIDName])

    # Create CSV from batchJobGroupList
    bjgColumns = ["ID", "BATCH_JOB_GROUP", "JOB_PLAN_ID", 'JOB_PLAN_NAME']
    bjgDF = pd.DataFrame(batchJobGroupList, columns=bjgColumns)
    bjgDF = bjgDF.set_index('ID')
    bjgDF.to_csv(outputCSVFile)

if __name__ == '__main__':
    getBatchJobGroups('XMLs\PROD_2022_10_12.xml', 'outputCSV\PathNames_PROD_20221012.csv', 'outputCSV\Batch_Job_Groups_PROD_1.csv')
    