import xml.etree.ElementTree as ET
from createCSV import createCSV

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()

Objects = root.iter('Object')

scheduleDict = {}
scheduleList = []

# Iterate through every Object element 
for obj in Objects:
    # Store JobPlan Objects in dictionary with {ID : name}
    if obj.get('typeid') == 'Schedule':
        ID = obj.find('ID').text
        name = obj.find('Name').text
        scheduleDict.update({ID : name})

print(scheduleDict)

# jobPlanColumns = ["Job Plan ID", "Job Plan Name"]

# createCSV(scheduleList, scheduleDict, jobPlanColumns, 'outputCSV\Job_Plans.csv')