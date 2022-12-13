import gviz_api
from datetime import *
from sql_to_dataframe import sql_to_dataframe
from create_main_pages import page_template

def create_timeline_page(sql_path):
	timeline_js = \
"""google.charts.load('current', {'packages':['timeline']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
	%(jscode)s

	var options = {
		timeline: {
			groupByRowLabel: true
		},
		avoidOverlappingGridLines: false,
	};

	var jscode_timeline = new google.visualization.Timeline(document.getElementById('table_div_jscode'));
	jscode_timeline.draw(jscode_data, options);
}
	"""

	page_title = 'Timeline'
	plan_page_path = ''
	description = ''
	last_update_datetime = datetime.now().strftime("%m/%d/%Y @ %H:%M:%S")
	legend = ''
	body_content = '<div id="table_div_jscode" class="vh-100"></div>'

	# Define field names for the timeline
	field_names = [('name', 'string'), ('start_time', 'datetime'), ('end_time', 'datetime')]

	# Fill data array with scheduled plans and their start and end times
	df = sql_to_dataframe(sql_path)
	data = []

	# Loop through every row in the dataframe and extract times 
	# and append it to data array
	for i in range(len(df)):
		plan = df.iloc[i]
		name = plan['NAME']
		times = plan['ENTIRE_SCHEDULES'].split('; ')
		for time in times:
			start_time = datetime.strptime(time, '%I:%M %p')
			end_time = start_time + timedelta(seconds=60)
			data.append([name, start_time, end_time])

	# Loading it into gviz_api.DataTable
	data_table = gviz_api.DataTable(field_names)
	data_table.LoadData(data)

	# Create a JavaScript code string.  
	jscode = data_table.ToJSCode("jscode_data",
								columns_order=("name", "start_time", "end_time"),
								order_by="start_time")

	# Put the JS code and JSON string into the template.
	with open(r'html_pages\webpages\timeline.js', 'w') as f:
		f.write(timeline_js % vars())

	with open(r'html_pages\webpages\timeline.html', 'w') as f:
		f.write(page_template % vars())

if __name__ == '__main__':
	create_timeline_page('html_pages\SQL_queries\SCHEDULED_PLANS_TIMELINE.sql')