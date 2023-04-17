import psycopg2

# Задание -:
# Функция, показывающая всех клиентов по ограничению лимита.

def all_clients(cur, limit):
        print(f'Список пользователей:\nId, Имя, Фамилия, Email, Номер телефона (если есть):')
        cur.execute('''SELECT * FROM clients c FULL JOIN phone p on p.client_id = c.id limit %s''', [limit])
        rows2 = cur.fetchall()
        return('\n'.join(map(str, rows2)))

# Задание 1:
# Функция, создающая структуру БД (таблицы).

def create_db(cur):
        cur.execute('''CREATE TABLE Clients(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(80) NOT NULL,
            surname VARCHAR(80) NOT NULL,
            email VARCHAR(80) NOT NULL)''')
        cur.execute('''CREATE TABLE Phone(
            phone_number VARCHAR(20) NOT NULL,
            Client_id integer NOT NULL references Clients(id)''')
        pass

# Задание 2:
# Функция, позволяющая добавить нового клиента.

def add_client(cur, firstname, surname, email, phone):
    values = (firstname, surname, email)
    cur.execute('''INSERT INTO clients (firstname, surname, email) VALUES (%s, %s, %s) RETURNING id''', values),
    new_id = cur.fetchone()[0]
    if phone != '':
        cur.execute('''INSERT INTO Phone (phone_number, client_id) VALUES (%s, %s)''', [phone, new_id])
    return('Клиент успешно добавлен')

# Задание 3:
# Функция, позволяющая добавить телефон для существующего клиента.

def add_phone(cur, client_id, phone_number):
    cur.execute("INSERT INTO phone (phone_number, client_id) VALUES (%s, %s)", [phone_number, client_id])
    return('Телефон успешно добавлен')

# Задание 4:
# Функция, позволяющая изменить данные о клиенте.

def change_client(cur, id, firstname=None, surname=None, email=None, phone1=None, phone2=None):

    id = int(input('Введите id:'))
    print()
    cur.execute('''SELECT * FROM clients WHERE id = %s''', [id])
    row = cur.fetchone()
    if row:
        print(f'ID: {row[0]}')
        print(f'Имя: {row[1]}')
        print(f'Фамилия: {row[2]}')
        print(f'Email: {row[3]}')
        print()
    else:
        print(f'Клиент с ID {id} не найден')
        print()

    text = (f'Какие данные хотите поменять:\n'
          f'1. Имя.\n'
          f'2. Фамилию.\n'
          f'3. Email.\n'
          f'4. Номер телефона.\n'
          f'0. Отмена\n')
    print(text)
    while True:
        try:
            command = int(input(f'Выберите команду: '))
            print()
            while command > 0:
                if command == 1:
                    firstname = input('Укажите новое имя:')
                    cur.execute('''UPDATE clients SET firstname = %s WHERE id = %s''', [firstname, id])
                    conn.commit()
                    print('Имя успешно изменено')
                    print()
                    print(text)
                elif command == 2:
                    surname = input('Укажите новую фамилию:')
                    cur.execute('''UPDATE clients SET surname = %s WHERE id = %s''', [surname, id])
                    conn.commit()
                    print('Фамилия успешна изменена')
                    print()
                    print(text)
                elif command == 3:
                    email = input('Укажите новый email :')
                    cur.execute('''UPDATE clients SET email = %s WHERE id = %s''', [email, id])
                    conn.commit()
                    print('email успешно изменен')
                    print()
                    print(text)
                elif command == 4:
                    cur.execute('''SELECT p.phone_number, p from phone p WHERE client_id = %s''', [id])
                    rows2 = cur.fetchall()
                    conn.commit()
                    for i, row in enumerate(rows2):
                        print(f"{i + 1}. {row[0]}")
                    phone_index = int(input('Укажите порядковый номер телефона для замены: ')) - 1
                    phone1 = rows2[phone_index][0]
                    phone2 = input('Введите новы номер:')
                    cur.execute(
                                '''UPDATE phone SET phone_number = %s WHERE client_id = %s AND phone_number = %s''',
                            [phone2, id, phone1])
                    print(f'Телефон {phone1} заменен на {phone2}')
                    print()
                    print(text)
                elif command == 0:
                    break
                else:
                    print('Такой команды не существует, \nВведите команду от 0 до 4\n')
                command = int(input('Выберите команду:'))
                print()
            print('Пока')
            break
        except ValueError:
            print(f'Упс, что то пошло не так, давайте еще разок\n')

# Задание 5:
# Функция, позволяющая удалить телефон для существующего клиента.

def delete_phone(cur, id, phone):
    cur.execute('''DELETE FROM phone WHERE client_id = %s and phone_number = %s''', [id, phone])
    pass

# Задание 6:
# Функция, позволяющая удалить существующего клиента.

def delete_client(cur, id):
    cur.execute('''DELETE FROM phone WHERE client_id = %s ''', [id]),
    cur.execute('''DELETE FROM clients WHERE id = %s ''', [id])
    pass

# Задание 7:
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.


def find_client(cur, firstname=None, surname=None, email=None, phone=None):
    if not any((firstname, surname, email, phone)):
        raise ValueError()
    params = []
    if firstname:
        params.append(('firstname', firstname))
    if surname:
        params.append(('surname', surname))
    if email:
        params.append(('email', email))
    if phone:
        params.append(('phone_number', phone))
    query = '''SELECT * FROM clients c FULL JOIN phone p on p.client_id = c.id WHERE '''
    for i, param in enumerate(params):
        if i > 0:
            query += ''' AND '''
        elif i < 0:
            query = '''SELECT * FROM clients c FULL JOIN phone p on p.client_id = c.id'''
        query += '''{} = %s'''.format(param[0])
    cur.execute(query, [p[1] for p in params])
    rows = cur.fetchall()
    print(rows)
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
    if __name__ == '__main__':
        comands_code()
        with conn.cursor() as cur:
            while True:
                try:
                    command = int(input(f'Выберите команду: '))
                    print()
                    while command > 0:
                        if command == 1:
                            print(all_clients(cur, limit=int(input('Сколько клиентов вывести'))), '\n')
                        elif command == 2:
                            print(create_db(cur), '\n')
                        elif command == 3:
                            print(add_client(cur, firstname=input('Имя:'), surname=input('Фамилия'), email=input('mail'),
                                             phone=input('phone')), '\n')
                        elif command == 4:
                            print(add_phone(cur, client_id=int(input('ID клиента')), phone_number=input('Номер телефона')),
                                  '\n')
                        elif command == 5:
                            change_client(cur, id)
                        elif command == 6:
                            print(delete_phone(cur, id=int(input('ID клиента')), phone=input('phone')), '\n')
                        elif command == 7:
                            print(delete_client(cur, id=int(input('ID клиента'))), '\n')
                        elif command == 8:
                            print(find_client(cur, firstname=input('Имя:'), surname=input('Фамилия'), email=input('mail'),
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
        conn.commit()


with psycopg2.connect(database = "DZBD5BAZA", user = "postgres", password = "") as conn:
    command_bd(conn, command = ())

conn.close()
