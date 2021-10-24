from App import conn, cur

with open('bingoClassSqlFile.sql') as f:
    conn.executescript(f.read())

cur.execute("""INSERT INTO sex(sex_type) VALUES("male") """)
cur.execute("""INSERT INTO sex(sex_type) VALUES("female") """)
cur.execute("""INSERT INTO sex(sex_type) VALUES("others") """)
cur.execute("SELECT * FROM sex")
records = cur.fetchall()
for rows in records:
    print(rows)

cur.execute("""INSERT INTO selling_opt(selling_type) VALUES("fixed_price") """)
cur.execute("""INSERT INTO selling_opt(selling_type) VALUES("Auction") """)
cur.execute("""INSERT INTO selling_opt(selling_type) VALUES("Donate") """)
cur.execute("SELECT * FROM selling_opt")
records = cur.fetchall()
for rows in records:
    print(rows)



cur.execute("""INSERT INTO categories(category_name) VALUES("Essentials") """)
cur.execute("""INSERT INTO categories(category_name) VALUES("Electronics") """)
cur.execute("""INSERT INTO categories(category_name) VALUES("Sports") """)
cur.execute("""INSERT INTO categories(category_name) VALUES("Cycles") """)
cur.execute("""INSERT INTO categories(category_name) VALUES("Clothing") """)
cur.execute("""INSERT INTO categories(category_name) VALUES("Books") """)
cur.execute("""INSERT INTO categories(category_name) VALUES("Bags") """)

cur.execute("SELECT * FROM categories")
records = cur.fetchall()
for rows in records:
    print(rows)

cur.execute("""INSERT INTO tags(tag_name) VALUES("Bucket") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("Mug") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("Mugs") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("Curtains") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("Matress") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("Bedsheet") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("Pillows") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("laundrybag") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("bottle") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("laptop") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("charger") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("lancable") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("adapter") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("extension") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("cable") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("jhalar") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("soapcase") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("wire") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("usb") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("phone") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("mobile") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("mobilecover") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("pendrive") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("badminton") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("tennis") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("ball") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("racket") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("cricketball") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("shuttlecock") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("shuttlecock feather") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("chess") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("bat") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("cycle") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("cyclelock") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("Bags") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("table") """)
cur.execute("""INSERT INTO tags(tag_name) VALUES("board") """)


cur.execute("SELECT * FROM tags")
records = cur.fetchall()
for rows in records:
    print(rows)


# inserting a dummy test user into the database to test for chat functionality while developing
query = """INSERT INTO user(user_id, first_name, last_name, email, contact_no, roll_no, valid) VALUES(?,?,?,?,?,?,?) """
data = ['test-rollnumber', 'Jhonny', 'Sins', 'test@gmail.com', 919876543210, 12345, True]
cur.execute(query, data)

query = """INSERT INTO user(user_id, first_name, last_name, email, contact_no, roll_no, valid) VALUES(?,?,?,?,?,?,?) """
data = ['test-rollnumber1', 'Nihal', 'Sargaiya', 'test1@gmail.com', 919876543219, 12346, True]
cur.execute(query, data)
conn.commit()
        

        



