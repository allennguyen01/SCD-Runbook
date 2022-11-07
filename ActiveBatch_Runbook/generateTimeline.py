import gviz_api
from datetime import *
from sql_to_dataframe import sql_to_dataframe
import sys
sys.path.insert(1, r'C:\Users\alnguyen\OneDrive - BCI\XML Batch Problem\DataTables_Website')
# from generateHTMLPages import page_template
from generateHTMLPages import page_template

def generateTimeline(sqlPath):
  timelineJS = """
  google.charts.load('current', {'packages':['timeline']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    %(jscode)s

    var options = {
      height: 3000,
      width: 1800,
      timeline: {
        groupByRowLabel: true
      },
      avoidOverlappingGridLines: false,
    };

    var jscode_timeline = new google.visualization.Timeline(document.getElementById('table_div_jscode'));
    jscode_timeline.draw(jscode_data, options);
  }
  """

  pageTitle = 'Timeline'
  planPagePrefix = ''
  description = ''
  legend = ''
  bodyContent = '<div id="table_div_jscode"></div>'

  # Define field names for the timeline
  fieldNames = [('name', 'string'), ('start_time', 'datetime'), ('end_time', 'datetime')]

  # Fill data array with scheduled plans and their start and end times
  df = sql_to_dataframe(sqlPath)
  data = []

  # Loop through every row in the dataframe and extract times 
  # and append it to data array
  for i in range(len(df)):
    plan = df.iloc[i]
    name = plan['NAME']
    if name == 'FLS_POS_HOLDINGS':
      continue
    startTime = plan['TIMES']
    duration = timedelta(days=0, seconds=60)
    endTime = startTime + duration
    data.append([name, startTime, endTime])

  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(fieldNames)
  data_table.LoadData(data)

  # Create a JavaScript code string.  
  jscode = data_table.ToJSCode("jscode_data",
                               columns_order=("name", "start_time", "end_time"),
                               order_by="start_time")

  # Put the JS code and JSON string into the template.
  with open('DataTables_Website\webpages\\timeline.js', 'w') as f:
    f.write(timelineJS % vars())

  with open('DataTables_Website\webpages\\timeline.html', 'w') as f:
    f.write(page_template % vars())

if __name__ == '__main__':
  generateTimeline('ActiveBatch_Runbook\SCHEDULED_PLANS.sql')