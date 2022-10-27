import csv

def createCSV(list, dict, colArr, fileName):
    for id in dict:
        tempDict = {}
        for colIdx in range(len(colArr)):
            colName = colArr[colIdx]
            colValue = id if colIdx == 0 else dict[id] if len(colArr) == 2 else dict[id][colIdx-1]
            tempDict.update({colName : colValue})
        list.append(tempDict)

    # Open empty CSV file
    csvFile = open(fileName, 'w', newline='')

    # Write header and rows to CSV from list
    with csvFile:
        jobPlanColumn = colArr
        writer = csv.DictWriter(csvFile,fieldnames=jobPlanColumn)
        writer.writeheader()
        writer.writerows(list)