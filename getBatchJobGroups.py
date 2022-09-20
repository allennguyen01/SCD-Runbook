import xml.etree.ElementTree as ET
import csv
from getJobPlans import jobPlanDict

tree = ET.parse('XMLs/BREAKFIX_20220913.xml')
root = tree.getroot()

Objects = root.iter('Object')

batchJobGroupDict = {}
batchJobGroupList = []

# Iterate through every Object element 
for obj in Objects:
    # Store Batch Job Groups in dictionary with {ID: [name, PID]}
    if obj.get('typeid') == 'Reference':
        target = obj.find('Target').find('ID')
        target = target.text if (target is not None) else ''
        if target == '15101103':
            name = obj.find('Name').text
            ID = obj.find('ID').text
            PID = obj.find('PID').find('ID').text
            # path = obj.find('Tags').find('Variable').find('Value').find('PID').find('Path')
            # path = path.text if (path is not None) else ''
            batchJobGroupDict.update({ID: [name, PID]})

# Create a list of all Batch Job Groups as dictionaries
for bjg in batchJobGroupDict:
    bjgName = batchJobGroupDict[bjg][0]
    jpID = batchJobGroupDict[bjg][1]
    jpName = jobPlanDict[jpID]
    # parentPath = batchJobGroupDict[bjg][2]
    # targetID = batchJobGroupDict[bjg][3]
    batchJobGroupList.append({"Batch Job Group ID" : bjg, "Batch Job Group Name" : bjgName, "Job Plan ID" : jpID, 'Job Plan Name' : jpName})

# Create empty CSV file
batchJobGroupCSV = open('outputCSV\Batch_Job_Groups.csv', 'w', newline='')

# Write CSV of batch job groups with ID, Name, and Job Plan ID as columns
with batchJobGroupCSV:
    batchJobColumns = ["Batch Job Group ID", "Batch Job Group Name", "Job Plan ID", 'Job Plan Name']
    writer = csv.DictWriter(batchJobGroupCSV, fieldnames=batchJobColumns)
    writer.writeheader()
    writer.writerows(batchJobGroupList)

# print(jobPlanDict)
# print(batchJobGroupDict)