# from types import NoneType
import xml.etree.ElementTree as ET
import tabulate

tree = ET.parse('XMLs\ABAT_BREAKFIX_SCD_SOD.xml')
root = tree.getroot()

# jobPlan = root[0].findall('Object')
Objects = root.iter('Object')

# print(Objects[0])

# for x in jobPlan:
#     print(x.attrib)

jobPlanDict = {}
batchJobGroupDict = {}
pidDict = {}

# Iterate through every Object element 
for obj in Objects:
    typeid = obj.get('typeid')
    # Store JobPlan Objects in dictionary with {ID : name}
    if obj.get('typeid') == 'JobPlan':
        ID = obj.find('ID').text
        name = obj.find('Name').text
        jobPlanDict.update({ID : name})
    # Store Reference Objects in dictionary with {ID: [name, PID]}
    if obj.get('typeid') == 'Reference':
        name = obj.find('Name').text
        ID = obj.find('ID').text
        PID = obj.find('PID').find('ID').text
        batchJobGroupDict.update({ID: [name, PID]})
    if  typeid == 'Reference' or 'JobPlan' or 'Plan':
        name = obj.find('Name').text
        PID = obj.find('PID').find('ID').text
        pidDict.update({name : PID})

# for obj in Objects:
#     typeid = obj.get('typeid')
#     if typeid == 'Reference' or typeid == 'Plan' or typeid == 'JobPlan':
#         name = obj.find('Name').text
#         PID = obj.find('PID').find('ID').text
#         pidDict.update({PID : name})


# def createPathName():


print(jobPlanDict)
print(batchJobGroupDict)
print(pidDict)