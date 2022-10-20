import xml.etree.ElementTree as ET
import csv
import pandas as pd
# from getJobPlans import jobPlanDict

def getBatchJobGroups(inXML, pathNameCSV, outCSV):
    tree = ET.parse(inXML)
    root = tree.getroot()
    pathNameDF = pd.read_csv(pathNameCSV, index_col='ID')
    bjgColumns = ["ID", "BATCH_JOB_GROUP", "JOB_PLAN_ID", 'JOB_PLAN_NAME']

    Objects = root.iter('Object')

    batchJobGroupList = []

    # Iterate through every Object element 
    for obj in Objects:
        # If object is of Reference type, get the data of the object
        if obj.get('typeid') == 'Reference':
            name = obj.find('Name').text
            ID = obj.find('ID').text
            PID = obj.find('PID').find('ID').text
            parentObj = pathNameDF.loc[int(PID)]
            if parentObj['OBJECT_TYPE'] != 'JobPlan':
                continue
            PIDName = pathNameDF.loc[int(PID)]['NAME'] if PID != '12249833' else ""
            batchJobGroupList.append([ID, name, PID, PIDName])

    # Create CSV from batchJobGroupList
    bjgDF = pd.DataFrame(batchJobGroupList, columns=bjgColumns)
    bjgDF = bjgDF.set_index('ID')
    bjgDF.to_csv(outCSV)

if __name__ == '__main__':
    getBatchJobGroups('XMLs\PROD_2022_10_12.xml', 'outputCSV\PathNames_PROD_20221012.csv', 'outputCSV\Batch_Job_Groups_PROD.csv')
    