import xml.etree.ElementTree as ET
import csv
import pandas as pd
# from getJobPlans import jobPlanDict

def get_batch_job_groups(xmlFile, pathnameCSVFile, outputCSVFile):
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
    bjgColumns = ["Batch Job Group ID", "Batch Job Group Name", "Job Plan ID", 'Job Plan Name']
    bjgDF = pd.DataFrame(batchJobGroupList, columns=bjgColumns)
    bjgDF = bjgDF.set_index('Batch Job Group ID')
    bjgDF.to_csv(outputCSVFile)

if __name__ == '__main__':
    get_batch_job_groups('XMLs\PROD_2022_10_12.xml', 'outputCSV\PathNames_PROD_20221012.csv', 'outputCSV\Batch_Job_Groups_PROD_1.csv')
    