import sqlite3

conn = sqlite3.connect('yoomoney.db')
cursor = conn.cursor()
conn.commit()


def db_table_val(token: str, account: str):
    try:
        cursor.execute(f"INSERT INTO tokens VALUES (?, ?)", (token, account))
        print(f'Токен {token} добавлен')
    except:
        print('Ошибка при добавлении токена.\nПроверьте валидность и правильность написания.\nОшибка получения ' 
              'номера.\nВозможно, данный токен имеется в базе данных. ')
    finally:
        conn.commit()


def db_table_delete(account: str):
    try:
        cursor.execute(f"DELETE FROM tokens WHERE account = '{account}'")
        return 'Выполнено'
    except:
        return 'Error'
    finally:
        conn.commit()


def db_delete_all():
    try:
        cursor.execute("SELECT access_token FROM tokens")
        data = cursor.fetchall()
        cursor.executemany(f"DELETE FROM tokens WHERE access_token = ?", data)
    except:
        return 'Error'
    finally:
        conn.commit()


def db_get_account(token: str):
    try:
        cursor.execute(f"SELECT account FROM tokens WHERE access_token = '{token}'")
        data = cursor.fetchall()
        return data[0][0]
    except:
        return 'Error'


def db_get_all():
    try:
        cursor.execute("SELECT access_token FROM tokens")
        data = cursor.fetchall()
        return data
    except:
        return 'Error'
