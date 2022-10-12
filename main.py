from getJobPlans import getJobPlans

if __name__ == '__main__':
    
    getJobPlans('XMLs\PROD_20221004.xml', 'outputCSV\Schedules_PROD.csv', 'outputCSV\JobPlans_PROD.csv')
    # getVariables('XMLs\PROD_20221004.xml', 'outputCSV\Variables_PROD.csv')

    # getPathNames('XMLs\PROD_20221004.xml', 'outputCSV\PathNames_PROD.csv')

    # # getExecutionOrder depends on PathNames csv
    # getExecutionOrder('XMLs\PROD_20221004.xml', 'outputCSV\PathNames_PROD.csv', 'outputCSV\ExecutionOrder_PROD.csv')
    