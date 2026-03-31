from connect import connect
import csv

def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))

    conn.commit()
    conn.close()


def load_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row[0], row[1]))

    conn.commit()
    conn.close()


def show():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    for row in cur.fetchall():
        print(row)

    conn.close()


def update():
    name = input("Кого изменить: ")
    new_phone = input("Новый номер: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, name))

    conn.commit()
    conn.close()


def delete():
    name = input("Кого удалить: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

    conn.commit()
    conn.close()


while True:
    print("\n1 add")
    print("2 load csv")
    print("3 show")
    print("4 update")
    print("5 delete")
    print("0 exit")

    c = input()

    if c == "1":
        add_contact()
    elif c == "2":
        load_csv()
    elif c == "3":
        show()
    elif c == "4":
        update()
    elif c == "5":
        delete()
    elif c == "0":
        break