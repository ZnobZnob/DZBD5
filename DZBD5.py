import psycopg2

# Задание -:
# Функция, показывающая всех клиентов по ограничению лимита.

def all_clients(conn, limit):
    with conn.cursor() as cur:
        print(f'Список пользователей:\nId, Имя, Фамилия, Email, Номер телефона (если есть):')
        cur.execute('''SELECT * FROM clients c FULL JOIN phone p on p.client_id = c.id limit %s''', [limit])
        rows2 = cur.fetchall()
        conn.commit()
    return('\n'.join(map(str, rows2)))

# Задание 1:
# Функция, создающая структуру БД (таблицы).

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE Clients(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(80) NOT NULL,
            surname VARCHAR(80) NOT NULL,
            email VARCHAR(80) NOT NULL)''')
        cur.execute('''CREATE TABLE Phone(
            phone_number VARCHAR(20) NOT NULL,
            Client_id integer NOT NULL references Clients(id)''')
        conn.commit()
    pass

# Задание 2:
# Функция, позволяющая добавить нового клиента.

def add_client(conn, firstname, surname, email, phone):
    values = (firstname, surname, email)
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO clients (firstname, surname, email) VALUES (%s, %s, %s) RETURNING id''', values),
        new_id = cur.fetchone()[0]
        if phone != '':
            cur.execute('''INSERT INTO Phone (phone_number, client_id) VALUES (%s, %s)''', [phone, new_id]),
        conn.commit()
    return('Клиент успешно добавлен')

# Задание 3:
# Функция, позволяющая добавить телефон для существующего клиента.

def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO phone (phone_number, client_id) VALUES (%s, %s)", [phone_number, client_id])
        conn.commit()
    return('Телефон успешно добавлен')

# Задание 4:
# Функция, позволяющая изменить данные о клиенте.

def change_client(conn, id, firstname=None, surname=None, email=None, phone1=None, phone2=None):
    values = (firstname, surname, email, id)
    with conn.cursor() as cur:
        cur.execute('''UPDATE clients SET firstname = %s, surname = %s, email = %s WHERE id = %s''', values)
        cur.execute('''UPDATE phone SET phone_number = REPLACE (phone_number, %s, %s) WHERE client_id = %s''', [phone1, phone2, id])
        conn.commit()
    pass

# Задание 5:
# Функция, позволяющая удалить телефон для существующего клиента.

def delete_phone(conn, id, phone):
    with conn.cursor() as cur:
        cur.execute('''DELETE FROM phone WHERE client_id = %s and phone_number = %s''', [id, phone]),
        conn.commit()
    conn.close()
    pass

# Задание 6:
# Функция, позволяющая удалить существующего клиента.

def delete_client(conn, id):
    # id = input('id клиента')
    with conn.cursor() as cur:
        cur.execute('''DELETE FROM phone WHERE client_id = %s ''', [id]),
        cur.execute('''DELETE FROM clients WHERE id = %s ''', [id])
        conn.commit()
    pass

# Задание 7:
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def find_client(conn, firstname=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute(
            '''SELECT * FROM clients c FULL JOIN phone p on p.client_id = c.id WHERE firstname = %s or surname = %s or email = %s or phone_number = %s''',
            [firstname, surname, email, phone])
        rows = cur.fetchall()
        print(rows)
        conn.commit()
    pass

def comands_code():
    print((f'Список команд:\n'
          f'1. Показать клиентов.\n'
          f'2. Создать Базы Данных Clients и Phone\n'
          f'3. Создать нового клиента.\n'
          f'4. Добавить номер телефона клиенту.\n'
          f'5. Изменить данные клиента.\n'
          f'6. Удалить номер телефона клиента.\n'
          f'7. Удалить клиента.\n'
          f'8. Найти клиента.\n'
          f'9. Показать команды.\n'
          f'0. Выход\n'))

def command_bd(conn, command):
    comands_code()
    while True:
        try:
            command = int(input(f'Выберите команду: '))
            print()
            while command > 0:
                if command == 1:
                    print(all_clients(conn, limit=int(input('Сколько клиентов вывести'))), '\n')
                elif command == 2:
                    print(create_db(conn), '\n')
                elif command == 3:
                    print(add_client(conn, firstname=input('Имя:'), surname=input('Фамилия'), email=input('mail'),
                                     phone=input('phone')), '\n')
                elif command == 4:
                    print(add_phone(conn, client_id=int(input('ID клиента')), phone_number=input('Номер телефона')),
                          '\n')
                elif command == 5:
                    print(change_client(conn, id=int(input('ID клиента')), firstname=input('Имя:'),
                                        surname=input('Фамилия'), email=input('mail'), phone1=input('Заменить номер:'),
                                        phone2=input('Новый номер:')), '\n')
                elif command == 6:
                    print(delete_phone(conn, id=int(input('ID клиента')), phone=input('phone')), '\n')
                elif command == 7:
                    print(delete_client(conn, id=int(input('ID клиента'))), '\n')
                elif command == 8:
                    print(find_client(conn, firstname=input('Имя:'), surname=input('Фамилия'), email=input('mail'),
                                      phone=input('phone')), '\n')
                elif command == 9:
                    print(comands_code(),'\n')
                elif command == 0:
                    break
                else:
                    print('Такой команды не существует, \nВведите команду от 0 до 8\n')
                command = int(input('Выберите команду:'))
                print()
            print('Пока')
            break
        except ValueError:
            print(f'Упс, что то пошло не так, давайте еще разок\n')



with psycopg2.connect(database = "DZBD5BAZA", user = "postgres", password = "") as conn:
    command_bd(conn, command = ())

conn.close()
