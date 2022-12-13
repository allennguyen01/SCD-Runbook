from get_scheduled_plans import get_scheduled_plans
from get_variables import get_variables
from get_path_names import get_path_names
from get_execution_order import get_execution_order
from get_schedules import get_schedules
from get_file_triggers import get_file_triggers
from get_batch_job_group import get_batch_job_groups
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

    get_schedules(xmlFile, 'csv\Schedules.csv')
    print("Schedules.csv generated successfully!")

    get_path_names(xmlFile, 'csv\PathNames.csv')
    print("PathNames.csv generated successfully!")

    get_variables(xmlFile, 'csv\Variables.csv')
    print("Variables.csv generated successfully!")

    get_file_triggers(xmlFile, 'csv\FileTriggers.csv')
    print("FileTriggers.csv generated successfully!")

    get_scheduled_plans(xmlFile, 'csv\Schedules.csv', 'csv\ScheduledPlans.csv')
    print("ScheduledPlans.csv generated successfully!")

    get_batch_job_groups(xmlFile, 'csv\PathNames.csv', 'csv\BatchJobGroups.csv')
    print("BatchJobGroups.csv generated successfully!")
    
    print("All csv files generated successfully in csv folder.")