import errors
import functions
import create_table
import insert
import errors_handlers
import termcolor
import select
import helpers

while True:
    query = input('>>>')
    if not helpers.brackets(query):
        print(termcolor.colored('Brackets error', 'red'))
        continue
    try:
        if query[0:12] == 'CREATE TABLE':
            create_table.create_table(query)
            print(termcolor.colored('Success!', 'green'))
        elif query[0:6] == 'SELECT':
            output, columns = select.select(query)
            print(select.make_table(output, columns))
        elif query[0:11] == 'INSERT INTO':
            insert.insert(
                query)
            print(termcolor.colored('Success!', 'green'))
        else:
            print(termcolor.colored('incorrect', 'red'))
    except errors.DataBaseError as error:
        print(termcolor.colored(f'Error: {error}', 'red'))

# CREATE TABLE Users (user_id INT, username VARCHAR(100) NOT NULL);
# CREATE TABLE Orders (order_id INT, order_date DATE NOT NULL, user_id INT, FOREIGN KEY (user_id) REFERENCES Users(user_id));
