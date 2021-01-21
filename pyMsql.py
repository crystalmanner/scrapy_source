import pymysql
import pymysql.cursors


def msql_connector(handler):
    def connect_msql(*args, **kwargs):
        con = pymysql.connect(
            host="127.0.0.1",
            user="root",
            db="scabal",
            charset="utf8",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        ret = handler(con, *args, **kwargs)
        con.close()
        return ret

    return connect_msql


def insert_object_as_row(con, table, obj):
    cur = con.cursor()
    columns, values = [], []
    for key, value in obj.items():
        columns.append(key)
        if value is '':
            values.append('NULL')
        else:
            if type(obj[key]) == str:
                value = value.replace("'", "''")
                values.append(("'{}'").format(value))
            else:
                values.append(str(value))
    query = """
                INSERT INTO {} ({}) VALUES ({});
            """.format(table, ', '.join(columns), ', '.join(values))
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Error Insert Sql in =>", e)


def update_object_as_row(con, table, obj, key_name):
    cur = con.cursor()
    columns, values = [], []
    for key, value in obj.items():
        if key == 'cloth_pattern_number':
            continue
        columns.append(key)
        if type(obj[key]) == str:
            value = value.replace("'", "''")
            values.append(("'{}'").format(value))
        else:
            values.append(str(value))

    query = """
            UPDATE {} SET {} WHERE {}={};
    """.format(table, ', '.join([a + "=" + b for a, b in zip(columns, values)]), key_name, "'" + str(obj[key_name]) + "'")
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Error update sql in  =>", e)


@msql_connector
def save_scabal(con, data):

    # cloth_pattern_number + cloth_bunch is unique key
    try:
        cur = con.cursor()
        sql_select_query = """
                            SELECT * from scabal_template WHERE cloth_pattern_number = {0} and cloth_bunch={1}
        """.format("'" + str(data['cloth_pattern_number']) + "'","'" + str(data['cloth_bunch']) + "'")
        cur.execute(sql_select_query)
        record = cur.fetchone()
        if record is not None:
            update_object_as_row(con, 'scabal_template', data, 'cloth_pattern_number')
        else:
            insert_object_as_row(con, "scabal_template", data)
    except Exception as e:
        print("error in save_scabal =>", e)
