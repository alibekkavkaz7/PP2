from connect import connect
import json
import csv


# ===== ДОБАВИТЬ КОНТАКТ (с email и birthday) =====
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO contacts(name, email, birthday)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, email, birthday))

    cid = cur.fetchone()[0]

    # добавить в группу
    if group:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    conn.close()

    print("Contact added")


# ===== ПОИСК (все поля) =====
def search():
    val = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (val,))
    for row in cur.fetchall():
        print(row)

    conn.close()


# ===== ПОИСК ТОЛЬКО ПО EMAIL =====
def search_email():
    val = input("Email search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, email
        FROM contacts
        WHERE email ILIKE %s
    """, ('%' + val + '%',))

    for row in cur.fetchall():
        print(row)

    conn.close()


# ===== СОРТИРОВКА =====
def sort_contacts():
    field = input("Sort by (name/birthday/date): ")

    if field == "date":
        field = "created_at"

    conn = connect()
    cur = conn.cursor()

    query = f"""
        SELECT name, email, birthday, created_at
        FROM contacts
        ORDER BY {field}
    """

    cur.execute(query)

    for row in cur.fetchall():
        print(row)

    conn.close()


# ===== ДОБАВИТЬ ТЕЛЕФОН =====
def add_phone():
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))

    conn.commit()
    conn.close()


# ===== ПЕРЕМЕСТИТЬ В ГРУППУ =====
def move_group():
    name = input("Name: ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    conn.close()


# ===== ФИЛЬТР ПО ГРУППЕ =====
def filter_group():
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    conn.close()


# ===== ПАГИНАЦИЯ =====
def paginate_loop():
    limit = int(input("Limit: "))
    offset = 0

    conn = connect()
    cur = conn.cursor()

    while True:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

    conn.close()


# ===== EXPORT JSON =====
def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str)

    conn.close()
    print("Exported")


# ===== IMPORT JSON =====
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = connect()
    cur = conn.cursor()

    for row in data:
        name, email, birthday, group, phone, ptype = row

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, email, birthday))

        cid = cur.fetchone()[0]

        if group:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))

        if phone:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, phone, ptype or 'mobile'))

    conn.commit()
    conn.close()


# ===== CSV IMPORT =====
def import_csv():
    filename = input("CSV file: ")

    conn = connect()
    cur = conn.cursor()

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row['name']
            email = row['email']
            birthday = row['birthday']
            group = row['group']
            phone = row['phone']
            ptype = row['type']

            cur.execute("""
                INSERT INTO contacts(name, email, birthday)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (name, email, birthday))

            cid = cur.fetchone()[0]

            if group:
                cur.execute("CALL move_to_group(%s, %s)", (name, group))

            if phone:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (cid, phone, ptype))

    conn.commit()
    conn.close()
    print("CSV imported")


# ===== МЕНЮ =====
while True:
    print("\n1 add contact")
    print("2 search")
    print("3 add phone")
    print("4 move group")
    print("5 filter group")
    print("6 pagination")
    print("7 export json")
    print("8 import json")
    print("9 sort")
    print("10 search email")
    print("11 import csv")
    print("0 exit")

    c = input()

    if c == "1":
        add_contact()
    elif c == "2":
        search()
    elif c == "3":
        add_phone()
    elif c == "4":
        move_group()
    elif c == "5":
        filter_group()
    elif c == "6":
        paginate_loop()
    elif c == "7":
        export_json()
    elif c == "8":
        import_json()
    elif c == "9":
        sort_contacts()
    elif c == "10":
        search_email()
    elif c == "11":
        import_csv()
    elif c == "0":
        break