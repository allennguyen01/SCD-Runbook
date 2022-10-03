import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('XMLs\BREAKFIX_20220913.xml')
root = tree.getroot()
Objects = root.iter('Object')

jobPlanList = []
scheduleDict = pd.read_csv('outputCSV\Schedules.csv', index_col='ID')
print(scheduleDict)
print(type(scheduleDict.loc[15104836]))

# Iterate through every Object element 
for obj in Objects:
    # Store JobPlan Objects in dictionary with {ID : name}
    if obj.get('typeid') == 'JobPlan':
        ID = obj.find('ID').text
        name = obj.find('Name').text

        scheduleIDList = []
        for sch in obj.iter('Schedules'):
            for schID in sch.findall('ObjectID'):
                try:
                    scheduleIDList.append(schID.find('ID').text)
                except AttributeError:
                    print(ID, name)
                    continue
            
        if scheduleIDList == []:
            continue
        
        scheduleList = [scheduleDict.loc[int(schID)]['Schedule Name'] for schID in scheduleIDList]
        
        jobPlanList.append([ID, name, scheduleIDList, scheduleList])

jobPlanColumns = ["ID", "Job Plan Name", 'Schedule IDs', 'Schedules']

jobPlanDF = pd.DataFrame(jobPlanList, columns=jobPlanColumns)
jobPlanDF = jobPlanDF.set_index('ID')

jobPlanDF.to_csv('outputCSV/JobPlans_schedules.csv')