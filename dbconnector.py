import mysql.connector

cnx = None
cursor = None


def build_connection() -> 'mysql connection':
    #Must Always run first.
    global cnx, cursor
    #Set user and password to your MySQL credentials
    cnx = mysql.connector.connect(user='root', password='password', database='cs121')
    cursor = cnx.cursor()


def close_connection() -> None:
    #Must ALWAYS close after running a query
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_data(term, locations) -> bool:
    # receives data as:
    # token, [(0//1, 1), (0//2, 1, b) ] etc
    data_obj = {'term': term, 'locations': locations}
    data_str = "INSERT INTO web_index (term, locations) VALUES (%(term)s, %(locations)s) ON DUPLICATE KEY UPDATE locations = %(locations)s "
    cursor.execute(data_str, data_obj)
    return cursor.lastrowid is not None


def query_data(term) -> list:
    data_str = "SELECT locations FROM web_index WHERE term = %s"
    cursor.execute(data_str, [term])
    return cursor.fetchone()[0]



