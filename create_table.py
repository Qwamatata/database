import json
import termcolor
import errors
import helpers
# def create_table2(data: str):
#     split_data = data.split(' ')
#     if split_data[0] == 'create' and split_data[1] == 'table':
#         table_name = split_data[2]
#         structure = split_data[3:]
#         repeat_num = 1
#         structure_dic = {}
#         element_key = ''
#         end_marker = False
#         for element in structure:
#             if end_marker == False:
#                 if repeat_num == 1:
#                     element_key = element.split('(')[1]
#                 else:
#                     element_key = element
#                 structure_dic[element_key] = []
#                 end_marker = True
#             elif ',' not in element:
#                 structure_dic[element_key].append(element)
#             else:
#                 if repeat_num == len(structure):
#                     structure_dic[element_key].append(element.split(');')[0])  # FIXME
#                 else:
#                     structure_dic[element_key].append(element.split(',')[0])
#                 element_key = ''
#                 end_marker = False
#             repeat_num += 1
#         add_dic_to_json(table_name, structure_dic, 'data.json')


def create_table(query: str):
    query = query[13:]
    space_index = query.find(' ')
    table_name = query[0:space_index]
    structure = query[space_index + 2:-2]
    column_list = structure.split(', ')
    structure_dic = {}
    structure_dic["id"] = {"type": "INT", "unique": True, "not_null": True}
    structure_json = helpers.get_json_data('structure.json')
    for column in column_list:
        # FOREIGN KEY (user_id) REFERENCES Users(user_id));
        if 'FOREIGN KEY' in column:
            column = column[len('FOREIGN KEY') + 1:]
            column_parts = column.split(' REFERENCES ')
            column_name_local = column_parts[0][1:-1]
            if column_name_local not in structure_dic:
                raise errors.DataBaseError(f'Unknown column {column_name_local} in FOREIGN KEY')
            table_name_ref = column_parts[1].split('(')[0]
            column_ref = column_parts[1].split('(')[1].split(')')[0]
            if table_name_ref not in structure_json:
                raise errors.DataBaseError(f'Unknown table {table_name_ref}')
            if column_ref not in structure_json[table_name_ref]:
                raise errors.DataBaseError(f'Unknown column {column_ref} in table {table_name_ref}')
            structure_dic[column_name_local]["foreign key"] = {'table_name': table_name_ref, 'column_name': column_ref}
        else:
            split_column = column.split(' ')
            column_name = split_column[0]
            column_type = split_column[1]
            dic = {'type': column_type}
            if column_type[0:7] == 'VARCHAR':
                br1_index = column_type.find('(')
                br2_index = column_type.find(')')
                max_length = column_type[br1_index + 1:br2_index]
                column_type = column_type[0:br1_index]
                dic['type'] = column_type
                dic['max_length'] = max_length
            dic['unique'] = 'UNIQUE' in column
            dic['not_null'] = 'NOT NULL' in column
            structure_dic[column_name] = dic
    add_dic_to_json(table_name, structure_dic, 'structure.json')
    add_dic_to_json(table_name, [], 'data.json')


# ex: CREATE TABLE table_n (name VARCHAR(10), last_name VARCHAR(15));


def add_dic_to_json(key: str, dic: dict | list, file_name: str):
    file = open(file_name, 'r', encoding='UTF-8')
    json_dic = json.load(file)
    json_dic[key] = dic
    file.close()
    file = open(file_name, 'w', encoding='UTF-8')
    json.dump(json_dic, file, ensure_ascii=False, indent=4)
    file.close()
