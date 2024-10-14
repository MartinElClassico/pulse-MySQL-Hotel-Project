# utils/dict2SQLInputStr.py

# converts dictionary into a string that corresponds to an SQL INSERT INTO statement
def dict_to_sql_insert_str(table_name, sql_dict, auto_gen_key):
    if auto_gen_key == True: del sql_dict[(table_name + '_id')] # Shouldn't have it in INSERT statement if autogenerated.
    # corresponds to vales {} as in INSERT INTO [table_name] ({})
    l_fields = _formatValues(sql_dict.keys(), True)
    l_field_values = _formatValues(sql_dict.values(), False)
    # make list into the sql values part of the string
    fields_as_str = ', '.join(l_fields)
    field_values_as_str = ', '.join(l_field_values)
    # Construct the SQL query
    sql_query_str = "INSERT INTO {} ({}) VALUES ({});".format(table_name, fields_as_str, field_values_as_str)
    return sql_query_str

# cleans dict values so they can be used as SQL field values.
def _formatValues(dict_values, field: bool):
    l_sql_values = []
    for value in dict_values:
        #if string type then make it so that SQL also sees it as string, otherwise just cast to string.
        if isinstance(value, str):
            if field:
                 l_sql_values.append(value)
            else:
                l_sql_values.append("'" + value + "'")
        else:
            l_sql_values.append(str(value))
    return l_sql_values

# Main function to test the implementation
if __name__ == "__main__":
    # Test case: a sample dictionary with different types of values
    test_table_name = "users"
    
    test_sql_dict = {
        "user_id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "age": 30,
        "created_at": "2024-10-10"
    }
    
    # Call the function with autogenerated key (e.g., user_id is autogenerated)
    print("Test run with autogenerated key:")
    print(dict_to_sql_insert_str(test_table_name, test_sql_dict.copy(), auto_gen_key=True))
    
    # Call the function without autogenerated key
    print("\nTest run without autogenerated key:")
    print(dict_to_sql_insert_str(test_table_name, test_sql_dict.copy(), auto_gen_key=False))