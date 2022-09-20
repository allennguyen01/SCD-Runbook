import xml.etree.ElementTree as ET
from createCSV import createCSV

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()

Objects = root.iter('Object')

jobPlanDict = {}
jobPlanList = []

# Iterate through every Object element 
for obj in Objects:
    # Store JobPlan Objects in dictionary with {ID : name}
    if obj.get('typeid') == 'JobPlan':
        ID = obj.find('ID').text
        name = obj.find('Name').text
        jobPlanDict.update({ID : name})

jobPlanColumns = ["Job Plan ID", "Job Plan Name"]

createCSV(jobPlanList, jobPlanDict, jobPlanColumns, 'outputCSV\Job_Plans.csv')
