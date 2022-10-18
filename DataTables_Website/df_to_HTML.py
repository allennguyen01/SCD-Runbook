from sql_to_dataframe import sql_to_dataframe

# Convert a Dataframe to a HTML table and return the string
def df_to_HTMLTable(df):
    columnNames = df.columns.tolist()
    tabTab = f'\t\t'

    # Form the thead tag with column field names
    tableHead = f"{tabTab}<thead>\n\t{tabTab}<tr style=\"text-align: right;\">\n\t{tabTab}<th>INDEX</th><th>{'</th><th>'.join(columnNames)}</th></tr>\n{tabTab}</thead>"

    # Form the tbody tag with data rows
    tableBody = f"\n{tabTab}<tbody>\n"
    for i in range(len(df)):
        plan = df.iloc[i]
        data = [plan[colName] for colName in columnNames]
        data = ["" if value is None else value for value in data]
        name = data[0]

        # Add hyperlink to name field
        data[0] = f"<a href=\"/{name}\">{name}</a>"

        tableBody += f"\t{tabTab}<tr>\n\t\t{tabTab}<th>{i}</th>\n\t\t{tabTab}<td>{'</td><td>'.join(data)}</td>\n\t{tabTab}</tr>\n"
    tableBody += f"{tabTab}</tbody>\n"

    # Wrap table tag around thead and tbody
    table = f"<table border=\"1\" class=\"dataframe table table-hover table-bordered table-striped\" id=\"table_id\">\n{tableHead}{tableBody}{tabTab}</table>"
    
    return table

def main():
    schPlansDF = sql_to_dataframe('DataTables_Website\SCHEDULED_PLANS_FIXED.sql')
    print(df_to_HTMLTable(schPlansDF))

if __name__ == "__main__":
    main()


    