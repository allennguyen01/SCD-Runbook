import xml.etree.ElementTree as ET
import pandas as pd
from createCSV import createCSV

tree = ET.parse('XMLs\BREAKFIX_20220922.xml')
root = tree.getroot()

Objects = root.iter('Object')

varDict = {}
varList = []

# Iterate through every Object element 
for obj in Objects:
    ID = obj.find('ID').text
    name = obj.find('Name').text

    Variables = obj.find('Variables').iter('Variable')
    for var in Variables:
        varName = var.find('Name').text
        varValue = var.find('Value').text
        varList.append([ID, name, varName, varValue])

varDF = pd.DataFrame(varList, columns=['ID', 'Name', 'Variable Name', 'Value'])
print(varDF)
varDF.to_csv('outputCSV/Variables.csv', index=False)

# Create a list of all Job Plans as dictionaries
# pidColumns = ['ID', 'Name', 'PID', 'Type ID', 'Path Name']

# createCSV(varList, varDict, pidColumns, 'outputCSV\Path_Names_test_1.csv')