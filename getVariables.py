import xml.etree.ElementTree as ET
import pandas as pd

def getVariables(xmlFile, outputCSVFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    Objects = root.iter('Object')

    varList = []

    # Iterate through every Object object with typeid 'JobPlan' or 'Plan'
    for obj in Objects:
        typeid = obj.get('typeid')
        if typeid in {'JobPlan', 'Plan'}:
            ID = obj.find('ID').text
            name = obj.find('Name').text

            # Loop through every variable in the JobPlan or Plan object
            Variables = obj.find('Variables').iter('Variable')
            for var in Variables:
                varName = var.findtext('Name')
                varValue = var.findtext('Value')
                varList.append([ID, name, varName, varValue])

    # Output a CSV file with Pandas using varList
    varColumns = ['ID', 'NAME', 'VARIABLE_NAME', 'VARIABLE_VALUE']
    varDF = pd.DataFrame(varList, columns=varColumns)
    varDF = varDF.set_index("ID")
    varDF.to_csv(outputCSVFile, index_label="ID")

if __name__ == "__main__":
    getVariables('XMLs\PROD_20221004.xml', 'outputCSV\Variables_PROD_1.csv')