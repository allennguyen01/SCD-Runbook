from getScheduledPlans import getScheduledPlans
from getVariables import getVariables
from getPathNames import getPathNames
from getExecutionOrder import getExecutionOrder
from getSchedules import getSchedules
from getFileTriggers import getFileTriggers
from getBatchJobGroups import getBatchJobGroups
import os

if __name__ == '__main__':
    while True:
        try:
            xmlFile = input("What is the path of the XML file from ActiveBatch? ")
            f = open(xmlFile)
            break
        except FileNotFoundError:
            print("FileNotFoundError. XML file does not exists, try again.")
            
    try:
        os.mkdir("csv")
    except FileExistsError:
        print("'csv' folder already exists.")

    getSchedules(xmlFile, 'csv\Schedules.csv')
    print("Schedules.csv generated successfully!")

    getPathNames(xmlFile, 'csv\PathNames.csv')
    print("PathNames.csv generated successfully!")

    getVariables(xmlFile, 'csv\Variables.csv')
    print("Variables.csv generated successfully!")

    getFileTriggers(xmlFile, 'csv\FileTriggers.csv')
    print("FileTriggers.csv generated successfully!")

    getScheduledPlans(xmlFile, 'csv\Schedules.csv', 'csv\ScheduledPlans.csv')
    print("ScheduledPlans.csv generated successfully!")

    getBatchJobGroups(xmlFile, 'csv\PathNames.csv', 'csv\BatchJobGroups.csv')
    print("BatchJobGroups.csv generated successfully!")
    
    print("All csv files generated successfully in csv folder.")