import helpers
import errors_handlers


def select(query):
    """
    :param query: sql query
    :return: output:
    """
    query = query[7:-1]
    split_query = query.split(' FROM ')
    columns = split_query[0].split(', ')
    conditions = []
    if ' WHERE ' in query:
        split_query2 = split_query[1].split(" WHERE ")
        table_name = split_query2[0]
        condition = split_query2[1].split(' ')
        conditions.append(condition)
    else:
        table_name = split_query[1].split(' ')[0]

    if ' INNER JOIN ' in query:
        split_query3 = split_query[1].split(' INNER JOIN ')
        table_name = split_query3[0]
        split_query4 = split_query3[1].split(' ON ')
        join_table_name = split_query4[0]
        join_fields = split_query4[1].split(' WHERE ')[0]
        records = join_tables(columns, table_name, join_table_name, join_fields)
    else:
        data = helpers.get_json_data('data.json')
        records = data[table_name]
        for index in range(len(records)):
            records[index] = join_dicts(records[index], {}, table_name, '')



    if columns == ["*"]:
        if 'INNER JOIN' not in query:
            structure_json = helpers.get_json_data('structure.json')[table_name]
            columns = list(structure_json.keys())
        else:
            structure_json1 = helpers.get_json_data('structure.json')[table_name]
            structure_json2 = helpers.get_json_data('structure.json')[join_table_name]
            columns1 = list(structure_json1.keys())
            for index in range(len(columns1)):
                columns1[index] = f'{table_name}.{columns1[index]}'
            columns2 = list(structure_json2.keys())
            for index in range(len(columns2)):
                columns2[index] = f'{join_table_name}.{columns2[index]}'
            columns = columns1 + columns2

    output = []
    if 'INNER JOIN' not in query:
        for index in range(len(columns)):
            columns[index] = f'{table_name}.{columns[index]}'
    for dic in records:
        dic = to_select_the_required_fields(dic, columns)
        output.append(dic)

    if ' ORDER BY ' in query:
        split_query2: str = split_query[1].split(' ORDER BY ')[1]
        column = split_query2.split(' ')[0]
        output = helpers.sort_data(output, f'{table_name}.{column}')
    return output, columns


def make_table(output: list, columns: list):
    table = '|'
    max_sp = max(columns, key=get_len_text)
    output_list = []
    for dic in output:
        for key in dic:
            output_list.append(str(dic[key]))
    max_sp_output = max(output_list, key=get_len_text)
    result_max = max([max_sp, max_sp_output], key=get_len_text)
    for column in columns:
        table += f'{column + ' ' * (len(result_max) - len(column))}|'
    table += '\n'
    length_string = len(result_max) * len(columns) + len(columns) + 1
    table += '-' * length_string + '\n'
    for dic in output:
        for element in columns:
            table += f'|{str(dic[element]) + ' ' * (len(result_max) - len(str(dic[element])))}'
        table += '|\n'

    return table


def get_len_text(text: str):
    return len(text)


def to_select_the_required_fields(database_entry: dict, list_of_fields: list) -> dict:
    """
    The function takes one record (in the form of a dictionary) and a list of field names.
    The function returns a new dictionary consisting of the first record's elements
    that are present in the list of fields.
    :param database_entry: #ex. {"id": 1, "name": "ivan", "last_name": "ivanov"}
    :param list_of_fields: #ex.  ["name", "last_name"]
    :return: #ex. {"name": "ivan", "last_name": "ivanov"}
    """
    return_dic = {}
    for key in database_entry:
        if key in list_of_fields:
            return_dic[key] = database_entry[key]
    return return_dic


def check_condition(record: dict, condition: list) -> bool:
    column_and_table_name, operator, value = condition
    table_name = column_and_table_name.split('.')[0]
    column = column_and_table_name.split('.')[1]
    result = helpers.compare_data(record[column_and_table_name], value, helpers.get_type(table_name, column))
    return operator == result


def check_conditions(record: dict, conditions: list) -> bool:
    for condition in conditions:
        if not check_condition(record, condition):
            return False
    return True


def sort_output_by_column(output: list[dict], column: str) -> list[dict]:
    pass


def join_dicts(dic1: dict, dic2: dict, table_name1: str, table_name2: str) -> dict:
    return_dic = {}
    for element in dic1:
        return_dic[f"{table_name1}.{element}"] = dic1[element]
    for element in dic2:
        return_dic[f"{table_name2}.{element}"] = dic2[element]
    return return_dic


def delete_useless_from_dict(columns: list, dic: dict) -> dict:
    return_dic = {}
    for column in columns:
        return_dic[column] = dic[column]
    return return_dic


def join_tables(columns: list, table1: str, table2: str, fields: str) -> list[dict]:
    fields = fields.split(' = ')
    field1 = fields[0].split('.')[1]
    field2 = fields[1].split('.')[1]
    data = helpers.get_json_data('data.json')
    join_dicts_list = []
    for record1 in data[table1]:
        for record2 in data[table2]:
            if record1[field1] == record2[field2]:
                join_dic = join_dicts(record1, record2, table1, table2)
                join_dicts_list.append(join_dic)

    return join_dicts_list
# SELECT name, last_name FROM table_n WHERE date_of_birth > 2025-09-05;
#
# SELECT employees.id, employees.name, departments.department_name FROM employees INNER JOIN departments ON employees.department_id = departments.id;
