import psycopg2


def handle_database(query_text, query_data):
    result = {}
    connect_str = "dbname='en' user='en' host='localhost'"
    connection = init_db(connect_str)
    if connection == 'connection error':
        result['result'] = 'Connection error. Server can not make a connection.'
        return result
    else:
        try:
            connection.autocommit = True
            cursor = connection.cursor()
            query = cursor.mogrify(query_text, query_data)
            cursor.execute(query)
            if "SELECT" in query_text:
                result['rows'] = cursor.fetchall()
                result['row_count'] = cursor.rowcount
            cursor.close()
            result['result'] = 'success'
        except Exception as e:
            result['result'] = e
        finally:
            return result


def init_db(connection_data):
    conn = None
    try:
        conn = psycopg2.connect(connection_data)
        return conn
    except Exception as e:
        return 'connection error'
