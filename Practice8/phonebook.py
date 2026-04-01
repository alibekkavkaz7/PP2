from connect import connect



def search():
    val = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (val,))
    for row in cur.fetchall():
        print(row)

    conn.close()

def upsert():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    conn.close()


def paginate():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)

    conn.close()



def delete():
    val = input("Name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (val,))

    conn.commit()
    conn.close()



while True:
    print("\n1 search")
    print("2 upsert")
    print("3 pagination")
    print("4 delete")
    print("0 exit")

    c = input()

    if c == "1":
        search()
    elif c == "2":
        upsert()
    elif c == "3":
        paginate()
    elif c == "4":
        delete()
    elif c == "0":
        break