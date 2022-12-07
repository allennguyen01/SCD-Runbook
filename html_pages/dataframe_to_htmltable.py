from sql_to_dataframe import sql_to_dataframe
config_df = sql_to_dataframe('html_pages\SQL_queries\SCD_CONFIG.sql')

# Convert a Dataframe to a HTML table and return the string
def dataframe_to_htmltable(df):
    columnNames = df.columns.tolist()

    tabTab = f'\t\t'

    # Form the thead tag with column field names
    tableHead = f"{tabTab}<thead>\n\t{tabTab}<tr style=\"text-align: right;\"><th>{'</th><th>'.join(columnNames)}</th></tr>\n{tabTab}</thead>"

    # Form the tbody tag with data rows
    tableBody = f"\n{tabTab}<tbody>\n"
    for i in range(len(df)):
        plan = df.iloc[i]
        data = [plan[colName] for colName in columnNames]
        data = ["" if value is None else value for value in data]

        firstCol = data[0]
        firstColArr = firstCol.split(' | ')
        batch_job_group = firstColArr[0]
        if (len(firstColArr) == 2): batch_job = firstColArr[1]

        # Add hyperlink to name field
        if (config_exists(batch_job_group) and columnNames[0] != 'Sort'):            
            if len(firstColArr) == 1:
                data[0] = f"<a href=\"plan_pages\{batch_job_group}.html\">{batch_job_group}</a>"
            elif len(firstColArr) == 2:
                data[0] = f"<a href=\"plan_pages\{batch_job_group}.html\">{batch_job_group}</a> | {firstColArr[1]}"
    
        tableBody += f"\t{tabTab}<tr>\n\t\t{tabTab}<td>{'</td><td>'.join(data)}</td>\n\t{tabTab}</tr>\n"
    tableBody += f"{tabTab}</tbody>\n"

    # Wrap table tag around thead and tbody
    table = f"<table border=\"1\" class=\"table table-hover table-bordered table-striped\" id=\"table_id\">\n{tableHead}{tableBody}{tabTab}</table>"
    
    return table

def config_exists(name):
    plan_config_df = config_df.loc[config_df['Batch Job Group'] == name]
    return not plan_config_df.empty

def main():
    schPlansDF = sql_to_dataframe('DataTables_Website\SCHEDULED_PLANS_FIXED.sql')
    print(dataframe_to_htmltable(schPlansDF))

if __name__ == "__main__":
    main()


    