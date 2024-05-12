def get_columns(cursor, table):
    # cursor.execute(f"pragma table_info('{table}')")
    # result = cursor.fetchall()
    # result = ([elem[1] for elem in result])
    # return result

    sql = f"SELECT * FROM {table}"
    cursor.execute(sql) 
    column_names = [desc[0] for desc in cursor.description] 
    return column_names 


def cols_to_string(cols):
    # return "'" + "', '".join([elem for elem in cols])+"'"
    return ", ".join([elem for elem in cols])



def select_query(cursor, table, arguments=None):
    if arguments:
        cursor.execute(f"SELECT * FROM {table} WHERE {arguments}")
    else:
        cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    return result


def insert_query(cursor, conn, table, values):
    columns = get_columns(cursor, table)
    datacount = ("%s, "*len(columns)).strip(", ")
    q = f"INSERT INTO {table} ({cols_to_string(columns)}) VALUES ({datacount})"
    ordered_values = [values[el] if el in values.keys(
    ) else None for el in columns]
    cursor.execute(q, ordered_values)
    conn.commit()

    # result = cursor.fetchall()
    # return result


def delete_query(cursor, conn, table, arguments=None):

    if arguments:
        cursor.execute(f"DELETE FROM {table} WHERE {arguments}")
    else:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    # result = cursor.fetchall()
    # return result


def update_query(cursor, conn, table, values, arguments=None):
    ordered_values = ", ".join(
        [f"`{key}`={val}" for key, val in values.items()])
    if arguments:
        q = f"UPDATE {table} SET {ordered_values} WHERE {arguments}"
        cursor.execute(q)
    else:
        cursor.execute(f"UPDATE {table} SET {ordered_values}")
    conn.commit()
    result = cursor.fetchall()
    return result