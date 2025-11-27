import json
import datetime


def get_json_data(file_name: str) -> dict:
    file = open(file_name, 'r', encoding='UTF-8')
    dic = json.load(file)
    file.close()
    return dic


def add_dic_to_json(key: str, dic: dict | list, file_name: str):
    file = open(file_name, 'r', encoding='UTF-8')
    json_dic = json.load(file)
    json_dic[key] = dic
    file.close()
    file = open(file_name, 'w', encoding='UTF-8')
    json.dump(json_dic, file, ensure_ascii=False, indent=4)
    file.close()


def save_json_data(file_name: str, dic: dict) -> None:
    file = open(file_name, 'w', encoding='UTF-8')
    json.dump(dic, file, ensure_ascii=False, indent=4)
    file.close()


def compare_data(value1: str, value2: str, datatype: str) -> str:
    type_converter = str
    if datatype == 'INT':
        type_converter = int

    if datatype == 'DATE':
        type_converter = date
    if type_converter(value1) > type_converter(value2):
        return '>'
    if type_converter(value1) < type_converter(value2):
        return '<'
    if type_converter(value1) == type_converter(value2):
        return '='


def date(value: str) -> datetime.date:
    split_date = value.split('-')
    return datetime.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))


def get_type(table_name: str, column: str) -> str:
    return get_json_data('structure.json')[table_name][column]['type']


def min_or_max_output(table_name_and_column: str, output: list, operator: str):
    table_name = table_name_and_column.split('.')[0]
    column = table_name_and_column.split('.')[1]
    structure = get_json_data('structure.json')[table_name][column]
    data_type = structure['type']
    max_dic = output[0]
    for dic in output:
        if compare_data(dic[table_name_and_column], max_dic[table_name_and_column], data_type) == operator:
            max_dic = dic
    return max_dic


def sort_data(output: list, table_name_and_column: str, operator: str = '>'):
    sort_output = []
    table_name = table_name_and_column.split('.')[0]
    column = table_name_and_column.split('.')[1]
    while len(output) != 0:
        new_output_value = min_or_max_output(table_name_and_column, output, operator)
        sort_output.append(new_output_value)
        output.remove(new_output_value)
    return sort_output


def brackets(text: str) -> bool:
    list_br = []
    brackets_types = {'(': ')', '[': ']', '{': '}'}
    brackets_string = ''
    for symbol in text:
        if symbol in '(){}[]':
            brackets_string += symbol
    for bracket in brackets_string:
        if len(list_br) != 0 and brackets_types[list_br[-1]] == bracket:
            list_br.pop(-1)
        else:
            list_br.append(bracket)
    return len(list_br) == 0

