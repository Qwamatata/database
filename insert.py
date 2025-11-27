import json
import helpers
import errors_handlers


def insert(query: str):
    table_name, columns, values = get_split_query(query)
    structure_dic = helpers.get_json_data('structure.json')

    errors_handlers.len_columns_values_err(columns, values)
    errors_handlers.table_not_found_err(table_name, structure_dic)
    errors_handlers.column_not_found_err(columns, structure_dic, table_name)
    errors_handlers.data_type_err(columns, table_name, values, structure_dic)
    errors_handlers.not_null_error(table_name, columns)

    data = {}
    for index in range(len(values)):
        data[columns[index]] = values[index]
    errors_handlers.unique_error(table_name, data)
    data_dic = helpers.get_json_data('data.json')
    table_info = data_dic[table_name]
    data["id"] = len(table_info) + 1
    table_info.append(data)
    helpers.save_json_data('data.json', data_dic)


def get_split_query(query):
    query = query[12:]
    space_index = query.find(' ')
    table_name = query[0:space_index]
    columns = query[query.find('(') + 1:query.find(')')].split(', ')
    query = query.split(' VALUES ')[1]
    values = query[1:-2].split(', ')
    print(values)
    return table_name, columns, values

# ex: INSERT INTO table_n (name, last_name) VALUES (ivan, ivanov);
# ex: INSERT INTO workers (name, email) VALUES (Ivan, example@123.com);
