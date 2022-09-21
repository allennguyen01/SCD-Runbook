import xml.etree.ElementTree as ET
from createCSV import createCSV

tree = ET.parse('XMLs\ABAT_BREAKFIX_SCD_SOD.xml')
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
        # pidName = obj.
        # scheduleID = obj.find('Schedules').find('ID').text
        Schedules = obj.iter('Schedules')
        for sch in Schedules:          
            scheduleID = obj.find('Tags').find('Variable').find('Value').find('Schedules').find('ObjectID').find('ID')
        scheduleID = scheduleID.text if (scheduleID is not None) else ''
        jobPlanDict.update({ID : [name, scheduleID]})

jobPlanColumns = ["Job Plan ID", "Job Plan Name", 'Schedule ID']

createCSV(jobPlanList, jobPlanDict, jobPlanColumns, 'outputCSV\Job_Plans_with_Schedules.csv')
