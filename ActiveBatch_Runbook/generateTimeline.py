#!/usr/bin/python

import gviz_api
from datetime import *
from sql_to_dataframe import sql_to_dataframe

page_template = """
<html>
  <script src="https://www.gstatic.com/charts/loader.js"></script>
  <script>
    google.charts.load('current', {'packages':['timeline']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
      %(jscode)s

      var options = {
        height: 3000,
        width: 1500,
        timeline: {
          groupByRowLabel: true
        }
      };

      var jscode_timeline = new google.visualization.Timeline(document.getElementById('table_div_jscode'));
      jscode_timeline.draw(jscode_data, options);
    }
  </script>
  <body>
    <H1>Weekday Scheduled Plans Timeline</H1>
    <div id="table_div_jscode"></div>
    
  </body>
</html>
"""

def main():
  # Define field names for the timeline
  description = [('name', 'string'), ('start_time', 'datetime'), ('end_time', 'datetime')]

  # Fill data with scheduled plans and their start and end times
  scheduled_plans = sql_to_dataframe('ActiveBatch_Runbook\SCHEDULED_PLANS.sql')
  data = []
  for i in range(len(scheduled_plans)):
    plan = scheduled_plans.iloc[i]
    name = plan['NAME']
    if name == 'FLS_POS_HOLDINGS':
      continue
    duration = timedelta(days=0, seconds=3600)
    startTime = plan['TIMES']
    endTime = startTime + duration
    data.append([name, startTime, endTime])

  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)

  # Create a JavaScript code string.  
  jscode = data_table.ToJSCode("jscode_data",
                               columns_order=("name", "start_time", "end_time"),
                               order_by="start_time")

  # Put the JS code and JSON string into the template.
  with open('ActiveBatch_Runbook\\runbook.html', 'w') as f:
    f.write(page_template % vars())

if __name__ == '__main__':
  main()