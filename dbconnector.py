import mysql.connector

cnx = None
cursor = None


def build_connection() -> 'mysql connection':
    #Must Always run first.
    global cnx, cursor
    #Set user and password to your MySQL credentials
    cnx = mysql.connector.connect(user='root', password='password', database='cs121', use_unicode=True)
    cursor = cnx.cursor(buffered=True)
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    cnx .commit()



def close_connection() -> None:
    #Must ALWAYS close after running a query
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_row(term, locations) -> bool:
    # receives data as:3
    # token, [(0//1, 1), (0//2, 1, b) ] etc
    data_obj = {'term': term, 'locations': locations}
    data_str = "INSERT INTO web_index (term, locations) VALUES (%(term)s, %(locations)s) ON DUPLICATE KEY UPDATE locations = %(locations)s"
    cursor.execute(data_str, data_obj)
    cnx.commit()
    return cursor.lastrowid is not None


def insert_all_data(file_name) -> bool:
    build_connection()
    db_query = "LOAD DATA LOCAL INFILE '" + str(file_name) + "' IGNORE INTO TABLE web_index " \
                                                             "FIELDS TERMINATED BY '|' " \
                                                             "LINES TERMINATED BY '\\r\\n'"
    cursor.execute(db_query)
    cnx.commit()
    ret = cursor.lastrowid is not None
    close_connection()
    return ret

def query_data(term) -> list:
    data_str = "SELECT locations FROM web_index WHERE term = %s"
    cursor.execute(data_str, [term])
    return cursor.fetchone()[0]



