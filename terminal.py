import main

while True:
    query = input('>>>')
    print(main.handle_query(query))

# CREATE TABLE Users (user_id INT, username VARCHAR(100) NOT NULL);
# CREATE TABLE Orders (order_id INT, order_date DATE NOT NULL, user_id INT, FOREIGN KEY (user_id) REFERENCES Users(user_id));
