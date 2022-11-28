import xml.etree.ElementTree as ET
import pandas as pd

def getScheduledPlans(xmlFile, schedulesCSVFile, outputCSVFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    Objects = root.iter('Object')

    scheduledPlansList = []
    scheduleDict = pd.read_csv(schedulesCSVFile, index_col='ID')

    # Iterate through every Object element with typeid JobPlan
    for obj in Objects:
        if obj.get('typeid') == 'JobPlan':
            ID = obj.findtext('ID')
            name = obj.findtext('Name')

            # Get all schedule IDs that run JobPlan and add them to scheduledPlansList
            for schedules in obj.iter('Schedules'):
                for sch in schedules.findall('ObjectID'):
                    schID = sch.findtext('ID')
                    schName = scheduleDict.loc[int(schID)]['ScheduleName']
                    scheduledPlansList.append([ID, schName])

    # Output a CSV file from scheduledPlansList using Pandas
    scheduledPlansColumns = ["ID", 'SCHEDULE']
    scheduledPlansDF = pd.DataFrame(scheduledPlansList, columns=scheduledPlansColumns)
    scheduledPlansDF = scheduledPlansDF.set_index('ID')
    scheduledPlansDF.to_csv(outputCSVFile)

if __name__ == "__main__":
    getScheduledPlans('XMLs\PROD_20221004.xml', 'outputCSV\Schedules_PROD.csv', 'outputCSV\SCHEDULED_PLANS_1.csv')