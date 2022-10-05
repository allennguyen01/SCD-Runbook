import xml.etree.ElementTree as ET
import pandas as pd

def getVariables(inXML, outVariablesCSV):
    tree = ET.parse(inXML)
    root = tree.getroot()
    Objects = root.iter('Object')

    varList = []

    # Iterate through every Object element 
    for obj in Objects:
        typeid = obj.get('typeid')
        if typeid == 'JobPlan' or typeid == 'Plan':
            ID = obj.find('ID').text
            name = obj.find('Name').text

            Variables = obj.find('Variables').iter('Variable')
            for var in Variables:
                varName = var.find('Name').text
                varValue = var.find('Value').text
                varList.append([ID, name, varName, varValue])

    varDF = pd.DataFrame(varList, columns=['ID', 'Name', 'Variable Name', 'Value'])
    varDF = varDF.set_index("ID")
    varDF.to_csv(outVariablesCSV, index_label="ID")

if __name__ == "__main__":
    getVariables('XMLs\PROD_20221004.xml', 'outputCSV\Variables_PROD.csv')