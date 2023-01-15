import psycopg2
from pprint import pprint

def create_db(conn):
    """Эта функция нужна для того, чтобы создать таблицы в базу данных"""

    with conn.cursor() as cur:
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
        # conn.commit()

def add_client(conn, name=None, surname=None, mail=None):
    """Эта функция нужна для того, чтобы добавить записи в поля таблицы 'client'"""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client (name, surname, mail) 
            VALUES
                (%s, %s, %s);
        """, (name, surname, mail,))
        # conn.commit()

def add_now_client_phone(conn, find_name, *args):
    """Эта функция нужна для того,чтобы добавить записи в поля таблицы 'phone_number'"""
    with conn.cursor() as cur:

        cur.execute("""
            select c.id_client
            from client c
            where c.name = %s
        """,(find_name,))
        try:
            find_id = cur.fetchall()[0][0]

            if len(args) >= 1:
                for phone_number in args:
                    cur.execute("""
                            INSERT INTO phone_number (phone_number, id_client)
                            VALUES
                            (%s, %s) RETURNING id_phone_number, phone_number, id_client
                        """,(phone_number, find_id,))
            else:
                print('Нет номера телефона')
        except:
            print('Ошибка при нахождении записи под таким индексом')

        # conn.commit()

def update_client(conn, id, name=None, surname=None, mail=None):
    """Эта функция нужна для обновления записи в таблицы 'client'"""
    with conn.cursor() as cur:
        if name is not None:
            cur.execute("""
                UPDATE client SET name=%s WHERE client.id_client=%s;
            """,(name, id,))
        if surname is not None:
            cur.execute("""
                UPDATE client SET surname=%s WHERE client.id_client=%s;
            """, (surname, id,))
        if mail is not None:
            cur.execute("""
                UPDATE client SET mail=%s WHERE client.id_client=%s;
            """, (mail, id,))


def delete_client_phone(conn, find_phone_number):
    """Эта функция нужна для удаления уже существующего номера телефона клиента"""
    with conn.cursor() as cur:
        cur.execute("""
                select pn.id_phone_number 
                from phone_number pn 
                where pn.phone_number = '{0}'
            """.format(find_phone_number))
        try:
            find_id = cur.fetchall()[0][0]
            cur.execute("""
                    DELETE
                    FROM phone_number pn
                    WHERE pn.id_phone_number = %s
                """, (find_id,))
            # conn.commit()
        except:
            print("Ошибка при нахождении записи в таблице 'phone_number', возможно неверно указано имя поля записи")

def delete_client(conn, find_client):
    """Эта функция удаляет запись в таблице 'client' и все связанные записи с ней"""
    with conn.cursor() as cur:
        try:
            cur.execute("""
                        select pn.id_phone_number
                        from phone_number pn  
                        where pn.id_client = (select c.id_client
                                              from client c
                                              where c.name = '{0}')
                    """.format(find_client))
            find_id = ()
            if find_id is None:
                for number in cur.fetchall():
                    find_id += number


                cur.execute("""
                    delete
                    from phone_number pn
                    where pn.id_phone_number in {0}
                        """.format(find_id))
            cur.execute("""
                select c.id_client
                from client c
                where c.name = '{0}'
            """.format(find_client))
            find_id_client = cur.fetchall()[0][0]
            cur.execute("""
                delete
                from client c
                where c.id_client = {0}
            """.format(find_id_client))
            # conn.commit()
        except:
            print("Ошибка при удалении клиента в таблице 'client'")

def find_client(conn, name=None, surname=None, mail=None, phone_number=None):
    with conn.cursor() as cur:
        info = None
        if name is not None:
            cur.execute("""
                select c.name, c.surname, c.mail, pn.phone_number 
                from client c join phone_number pn on pn.id_client = c.id_client 
                where c.name = %s
            """, (name,))
            info = cur.fetchall()
        elif surname is not None:
            cur.execute("""
                select c.name, c.surname, c.mail, pn.phone_number 
                from client c join phone_number pn on pn.id_client = c.id_client 
                where c.surname = %s
            """, (surname,))
            info = cur.fetchall()
        elif mail is not None:
            cur.execute("""
                select c.name, c.surname, c.mail, pn.phone_number 
                from client c join phone_number pn on pn.id_client = c.id_client 
                where c.mail = %s
            """, (mail,))
            info = cur.fetchall()
        elif phone_number is not None:
            cur.execute("""
                select c.name, c.surname, c.mail, pn.phone_number 
                from client c join phone_number pn on pn.id_client = c.id_client 
                where pn.phone_number = %s
            """, (phone_number,))
            info = cur.fetchall()
        else:
            print('Запись не найдена')

        print(info)
        # conn.commit()

if __name__ == '__main__':
    with psycopg2.connect(database="python_test", user='postgres', password='Wew019283746556') as conn:
        create_db(conn)

        add_client(conn, 'Bob', 'Booble', 'Bob64@gmail.com')
        add_client(conn, 'Vova', 'Booble', 'Bob64@gmail.com')

        update_client(conn, 2, 'igor', 'pop', 'pop@gmail.com')
        update_client(conn, 2, mail='yww@gmail.com')

        add_now_client_phone(conn, 'igor', '89288880809', '89288881111')
        add_now_client_phone(conn, 'Bob', '89288882222')

        delete_client_phone(conn, '89288882222')
        delete_client(conn, 'Bob')

        find_client(conn, phone_number='89288880809')
