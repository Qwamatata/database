import errors
import helpers
import datetime


def len_columns_values_err(columns: list, values: list):
    if len(columns) != len(values):
        raise errors.DataBaseError('The value does not match the columns')


def table_not_found_err(table_name: str, structure_dic: dict):
    if table_name not in structure_dic:
        raise errors.DataBaseError('table not found')


def column_not_found_err(columns: list, structure_dic: dict, table_name: str):
    for index in range(len(columns)):
        if columns[index] not in structure_dic[table_name]:
            raise errors.DataBaseError(f'column {columns[index]} not found')


def data_type_err(columns: list, table_name: str, values: list, structure_dic: dict):
    index = 0
    for column in columns:
        type_ = structure_dic[table_name][column]["type"]
        if type_ == 'VARCHAR':
            max_l = structure_dic[table_name][column]["max_length"]
            if int(max_l) < len(values[index]):
                raise errors.DataBaseError('VARCHAR err')
        elif type_ == 'INT':
            if not values[index].isdigit():
                raise errors.DataBaseError(
                    f'the data specified does not correspond to the type specified when creating the table column: {column} (VARCHAR instead of INT)')
        index += 1


def column_not_found_for_select_err(dic: dict, columns: list, index: int) -> None:
    if columns[index] not in dic:
        raise errors.DataBaseError(f'Column \"{columns[index]}\" not found')


def not_null_error(table_name: str, columns: list):
    structure = helpers.get_json_data('structure.json')[table_name]
    for column in structure:
        if structure[column]['not_null'] and column not in columns and column != 'id':
            raise errors.DataBaseError(f'Column \'{column}\' has restriction \'NOT NULL\'')


def unique_error(table_name: str, data: dict):
    structure: dict = helpers.get_json_data('structure.json')[table_name]
    table_data: list[dict] = helpers.get_json_data('data.json')[table_name]
    for column in data:
        if structure[column]["unique"]:
            for record in table_data:
                if record[column] == data[column]:
                    raise errors.DataBaseError(f'Column {column} not UNIQUE')
