from getScheduledPlans import getScheduledPlans
from getVariables import getVariables
from getPathNames import getPathNames
from getExecutionOrder import getExecutionOrder
from getSchedules import getSchedules
from getFileTriggers import getFileTriggers
from getBatchJobGroups import getBatchJobGroups


if __name__ == '__main__':
    xmlFile = input("What is the path of the XML file from ActiveBatch?")

    getSchedules(xmlFile, 'csv\Schedules.csv')
    getPathNames(xmlFile, 'csv\PathNames.csv')
    getVariables(xmlFile, 'csv\Variables.csv')
    getFileTriggers(xmlFile, 'csv\FileTriggers.csv')
    getScheduledPlans(xmlFile, 'csv\Schedules.csv', 'csv\ScheduledJobs.csv')
    getBatchJobGroups(xmlFile, 'csv\PathNames.csv', 'csv\BatchJobGroups.csv')
    
    print("All csv file generated successfully!")