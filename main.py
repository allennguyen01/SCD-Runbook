from getScheduledPlans import getScheduledPlans
from getVariables import getVariables
from getPathNames import getPathNames
from getExecutionOrder import getExecutionOrder
from getSchedules import getSchedules


if __name__ == '__main__':
    getSchedules('XMLs\PROD_20221004.xml', 'outputCSV\Schedules_PROD.csv')
    
    # depends on Schedules csv file
    getScheduledPlans('XMLs\PROD_20221004.xml', 'outputCSV\Schedules_PROD.csv', 'outputCSV\JobPlans_PROD.csv')

    getVariables('XMLs\PROD_20221004.xml', 'outputCSV\Variables_PROD.csv')

    getPathNames('XMLs\PROD_20221004.xml', 'outputCSV\PathNames_PROD.csv')

    # getExecutionOrder depends on PathNames csv file
    getExecutionOrder('XMLs\PROD_20221004.xml', 'outputCSV\PathNames_PROD.csv', 'outputCSV\ExecutionOrder_PROD.csv')
    