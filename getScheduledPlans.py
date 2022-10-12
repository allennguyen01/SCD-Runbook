import xml.etree.ElementTree as ET
import pandas as pd

def getJobPlans(inXML, inScheduleCSV, outJobPlanCSV):
    tree = ET.parse(inXML)
    root = tree.getroot()
    Objects = root.iter('Object')

    jobPlanList = []
    scheduleDict = pd.read_csv(inScheduleCSV, index_col='ID')

    # Iterate through every Object element 
    for obj in Objects:
        # Store JobPlan Objects in dictionary with {ID : name}
        if obj.get('typeid') == 'JobPlan':
            ID = obj.findtext('ID')
            name = obj.findtext('Name')

            # Get all schedule IDs of JobPlan and add them to a local list
            for schedules in obj.iter('Schedules'):
                for sch in schedules.findall('ObjectID'):
                    try:
                        schID = sch.findtext('ID')
                        schName = scheduleDict.loc[int(schID)]['ScheduleName']
                        # schTime = scheduleDict.loc[int(schID)]['Time']
                        # jobPlanList.append([ID, name, schID, schName, schTime])
                        jobPlanList.append([ID, schName])

                    except AttributeError:
                        print(ID, name)
                        continue

    # jobPlanColumns = ["ID", "Job Plan Name", 'Schedule ID', 'Schedule Name', 'Schedule Time']
    jobPlanColumns = ["ID", 'SCHEDULENAME']

    jobPlanDF = pd.DataFrame(jobPlanList, columns=jobPlanColumns)
    jobPlanDF = jobPlanDF.set_index('ID')

    jobPlanDF.to_csv(outJobPlanCSV)

if __name__ == "__main__":
    getJobPlans('XMLs\PROD_20221004.xml', 'outputCSV\Schedules_PROD.csv', 'outputCSV\SCHEDULED_PLANS.csv')