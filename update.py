# UPDATE Users SET username = example WHERE id = 3;
import helpers


def update(query: str):
    query = query[7:-1]
    table_name = query.split(' ')[0]
    column_name = query.split(' ')[2]
    value = query.split(' ')[4]
    if 'WHERE' in query:
        condition = query.split(' WHERE ')[1].split(' ')
        condition_column = condition[0]
        condition_operator = condition[1]
        condition_value = condition[2]
    json_file = helpers.get_json_data('data.json')
    records = json_file[table_name]
    for record in records:
        if ' WHERE ' in query:
            record_value = record[condition_column]
            if condition_operator == helpers.compare_data(record_value, condition_value, 'VARCHAR'):
                record[column_name] = value
        else:
            record[column_name] = value
    helpers.save_json_data('data.json', json_file)
