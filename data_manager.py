import psycopg2


def handle_database(command):
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
            cursor.execute(command)
            if "SELECT" in command:
                result['rows'] = cursor.fetchall()
                # result['column_names'] = [desc[0] for desc in cursor.description]
                result['row_count'] = cursor.rowcount
            cursor.close()
            result['result'] = 'success'
        except Exception as e:
            result['result'] = e
            print(e)
        finally:
            return result


def init_db(connection_data):
    conn = None
    try:
        conn = psycopg2.connect(connection_data)
        return conn
    except Exception as e:
        print(e)
        return 'connection error'
