# utils/dict2SQLInputStr.py

def dict_to_sql_insert_str(table_name, sql_dict):
    # corresponds to vales {} as in INSERT INTO [table_name] ({})
    fields_as_str = ', '.join(sql_dict.keys())
    l_field_values = _formatValues(sql_dict.keys())
    # make list into the sql values part of the string
    field_values_as_str = ', '.join(l_field_values)
    # Construct the SQL query
    sql_query_str = "INSERT INTO {} ({}) VALUES ({});".format(table_name, fields_as_str, field_values_as_str)
    return sql_query_str

# cleans dict values so they can be used as SQL field values.
def _formatValues(dict_values):
    l_sql_values = []
    for value in dict_values:
        #if string type then make it so that SQL also sees it as string, otherwise just cast to string.
        if isinstance(value, str):
            l_sql_values.append("'" + value + "'")
        else:
            l_sql_values.append(str(value))
    return l_sql_values

