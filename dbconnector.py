import mysql.connector

cnx = None
cursor = None


def build_connection() -> 'mysql connection':
    global cnx, cursor
    cnx = mysql.connector.connect(user='root', password='password', database='cs121')
    cursor = cnx.cursor()


def close_connection() -> None:
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_data(term, locations) -> bool:
    data_obj = {'term': term, 'locations': locations}
    data_str = "INSERT INTO web_index (term, locations) VALUES (%(term)s, %(locations)s)"
    cursor.execute(data_str, data_obj)
    return cursor.lastrowid is not None


def query_data(term) -> list:
    data_str = "SELECT locations FROM web_index WHERE term = %s"
    cursor.execute(data_str, [term])
    return cursor.fetchone()[0]



