import psycopg2
from pprint import pprint

def create_db(conn):
    cur = conn.cursor()
    cur.execute("""
        DROP TABLE IF EXISTS phone_number;
        DROP TABLE IF EXISTS client;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS client (
            id_client SERIAL primary key,
            name varchar(15) not null,
            surname varchar(15) not null,
            mail varchar(255)
            );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number (
            id_phone_number SERIAL primary key,
            phone_number varchar(12),
            id_client int not null references client(id_client)
            );
    """)
    print('Done! create_db')
    conn.commit()
    cur.close()

def add_client_and_phone_number(conn, name, surname, mail, *args):
    global count_phone, count_client
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO client (id_client, name, surname, mail) 
        VALUES
            ({0}, '{1}', '{2}', '{3}');
    """.format(count_client, name, surname, mail))


    if len(args) >= 1:
        for i in args:
            cur.execute("""
                    INSERT INTO phone_number (id_phone_number, phone_number, id_client)
                    VALUES
                        ({0}, '{1}', {2}) RETURNING id_phone_number, phone_number, id_client;
                """.format(count_phone, i, count_client))
            count_phone += 1
            print('Done! add_phone_number')
            print(cur.fetchall())
            print('Done! add_client')

    count_client += 1
    conn.commit()
    cur.close()

def add_now_client_phone(conn, find_name):
    cur = conn.cursor()

    cur.execute("""
        select c.id_client
        from client c
        where c.name = '{0}'
    """.format(find_name))
    find_id = cur.fetchall()[0][0]

    cur.execute("""
        UPDATE phone_number
        SET 
    """)

    conn.commit()
    cur.close()

def update_client(conn, id, name, surname, mail):
    cur = conn.cursor()

    cur.execute("""
        UPDATE client SET name='{0}', surname='{1}', mail='{2}' WHERE client.id_client = {3} ;
    """.format(name, surname, mail, id))
    print('Done! update_client')

    conn.commit()
    cur.close()

def update_phone_number():

    cur.execute("""
        UPDATE phone_number SET phone_number=%s;
    """, ('89286662232',))
    print('Done! update_phone_number')
    conn.commit()

def delete_client():
    cur.execute("""
        DELETE
        FROM phone_number pn
        WHERE pn.id_client=%s;
    """, (1,))

    cur.execute("""
            DELETE
            FROM client c
            WHERE c.id_client=%s;
        """, (1,))

    print('Done! delete_client')
    conn.commit()

def find_client(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM client c join phone_number pn on c.id_client = pn.id_client 
        WHERE c.id_client = 2
    """)
    pprint(cur.fetchall())
    conn.commit()
    cur.close()

if __name__ == '__main__':
    count_phone = 1
    count_client = 1
    with psycopg2.connect(database="python_test", user='postgres', password='Wew019283746556') as conn:
        create_db(conn)
        add_client_and_phone_number(conn, 'Bob', 'Booble', 'Bob64@gmail.com', '89288880809', '89288881111')
        add_client_and_phone_number(conn, 'Vova', 'Booble', 'Bob64@gmail.com', '89288882222')
        update_client(conn, 2, 'igor', 'pop', 'pop@gmail.com')
        add_now_client_phone(conn, 'igor')
        find_client(conn)



