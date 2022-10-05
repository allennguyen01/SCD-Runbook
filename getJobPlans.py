import xml.etree.ElementTree as ET
import pandas as pd

def getJobPlans(inXML, inScheduleCSV, outJobPlanCSV):
    tree = ET.parse(inXML)
    root = tree.getroot()
    Objects = root.iter('Object')

    jobPlanList = []
    scheduleDict = pd.read_csv(inScheduleCSV, index_col='ID')
    # print(scheduleDict)
    # print(type(scheduleDict.loc[15104836]))

    # Iterate through every Object element 
    for obj in Objects:
        # Store JobPlan Objects in dictionary with {ID : name}
        if obj.get('typeid') == 'JobPlan':
            ID = obj.findtext('ID')
            name = obj.findtext('Name')

            scheduleIDList = []

            # Get all schedule IDs of JobPlan and add them to a local list
            for sch in obj.iter('Schedules'):
                for schID in sch.findall('ObjectID'):
                    try:
                        scheduleIDList.append(schID.find('ID').text)
                    except AttributeError:
                        print(ID, name)
                        continue
            
            # If JobPlan is not triggered by a schedule, don't add to JobPlan list 
            if scheduleIDList == []:
                continue
            

            scheduleList = [scheduleDict.loc[int(schID)]['Schedule Name'] for schID in scheduleIDList]

            scheduleTimeList = [scheduleDict.loc[int(schID)]['Time'] for schID in scheduleIDList]
            
            jobPlanList.append([ID, name, scheduleIDList, scheduleList, scheduleTimeList])

    jobPlanColumns = ["ID", "Job Plan Name", 'Schedule IDs', 'Schedule Names', 'Schedule Times']

    jobPlanDF = pd.DataFrame(jobPlanList, columns=jobPlanColumns)
    jobPlanDF = jobPlanDF.set_index('ID')

    jobPlanDF.to_csv(outJobPlanCSV)

# getJobPlans('XMLs\PROD_20221004.xml', 'outputCSV\Schedules_prod.csv', 'outputCSV\JobPlans_prod.csv')

# getJobPlans('XMLs\BREAKFIX_20220913.xml', 'outputCSV\Schedules.csv', 'outputCSV\JobPlans_test.csv')