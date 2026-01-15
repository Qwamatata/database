import errors
import create_table
import insert
import helpers
import select_db
import update


def handle_query(query):
    if not helpers.brackets(query):
        return 'Brackets error'

    try:
        if query[0:12] == 'CREATE TABLE':
            create_table.create_table(query)
            return 'Success!'
        elif query[0:6] == 'SELECT':
            output, columns = select_db.select(query)
            return output, columns
        elif query[0:11] == 'INSERT INTO':
            insert.insert(
                query)
            return 'Success!'
        elif query[0:6] == 'UPDATE':
            update.update(query)
        else:
            return 'incorrect'
    except errors.DataBaseError as error:
        return f'Error: {error}'
