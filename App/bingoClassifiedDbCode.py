import sqlite3
def seedDB():
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()
	with open('SqlFile.sql') as f:
		conn.executescript(f.read())

	cur.execute("""INSERT INTO sex(name) VALUES("male") """)
	cur.execute("""INSERT INTO sex(name) VALUES("female") """)
	cur.execute("""INSERT INTO sex(name) VALUES("others") """)
	cur.execute("SELECT id,name FROM sex")
	records = cur.fetchall()
	for rows in records:
		print(rows)

	cur.execute("""INSERT INTO selling_opt(name) VALUES("fixed_price") """)
	cur.execute("""INSERT INTO selling_opt(name) VALUES("Auction") """)
	cur.execute("""INSERT INTO selling_opt(name) VALUES("Donate") """)
	cur.execute("SELECT * FROM selling_opt")
	records = cur.fetchall()
	# for rows in records:
	# 	print(rows)



	cur.execute("""INSERT INTO categories(name) VALUES("Essentials") """)
	cur.execute("""INSERT INTO categories(name) VALUES("Electronics") """)
	cur.execute("""INSERT INTO categories(name) VALUES("Sports") """)
	cur.execute("""INSERT INTO categories(name) VALUES("Cycles") """)
	cur.execute("""INSERT INTO categories(name) VALUES("Clothing") """)
	cur.execute("""INSERT INTO categories(name) VALUES("Books") """)
	cur.execute("""INSERT INTO categories(name) VALUES("Bags") """)

	cur.execute("SELECT * FROM categories")
	records = cur.fetchall()
	# for rows in records:
	# 	print(rows)

	cur.execute("""INSERT INTO tags(name) VALUES("Bucket") """)
	cur.execute("""INSERT INTO tags(name) VALUES("Mug") """)
	cur.execute("""INSERT INTO tags(name) VALUES("Mugs") """)
	cur.execute("""INSERT INTO tags(name) VALUES("Curtains") """)
	cur.execute("""INSERT INTO tags(name) VALUES("Matress") """)
	cur.execute("""INSERT INTO tags(name) VALUES("Bedsheet") """)
	cur.execute("""INSERT INTO tags(name) VALUES("Pillows") """)
	cur.execute("""INSERT INTO tags(name) VALUES("laundrybag") """)
	cur.execute("""INSERT INTO tags(name) VALUES("bottle") """)
	cur.execute("""INSERT INTO tags(name) VALUES("laptop") """)
	cur.execute("""INSERT INTO tags(name) VALUES("charger") """)
	cur.execute("""INSERT INTO tags(name) VALUES("lancable") """)
	cur.execute("""INSERT INTO tags(name) VALUES("adapter") """)
	cur.execute("""INSERT INTO tags(name) VALUES("extension") """)
	cur.execute("""INSERT INTO tags(name) VALUES("cable") """)
	cur.execute("""INSERT INTO tags(name) VALUES("jhalar") """)
	cur.execute("""INSERT INTO tags(name) VALUES("soapcase") """)
	cur.execute("""INSERT INTO tags(name) VALUES("wire") """)
	cur.execute("""INSERT INTO tags(name) VALUES("usb") """)
	cur.execute("""INSERT INTO tags(name) VALUES("phone") """)
	cur.execute("""INSERT INTO tags(name) VALUES("mobile") """)
	cur.execute("""INSERT INTO tags(name) VALUES("mobilecover") """)
	cur.execute("""INSERT INTO tags(name) VALUES("pendrive") """)
	cur.execute("""INSERT INTO tags(name) VALUES("badminton") """)
	cur.execute("""INSERT INTO tags(name) VALUES("tennis") """)
	cur.execute("""INSERT INTO tags(name) VALUES("ball") """)
	cur.execute("""INSERT INTO tags(name) VALUES("racket") """)
	cur.execute("""INSERT INTO tags(name) VALUES("cricketball") """)
	cur.execute("""INSERT INTO tags(name) VALUES("shuttlecock") """)
	cur.execute("""INSERT INTO tags(name) VALUES("shuttlecock feather") """)
	cur.execute("""INSERT INTO tags(name) VALUES("chess") """)
	cur.execute("""INSERT INTO tags(name) VALUES("bat") """)
	cur.execute("""INSERT INTO tags(name) VALUES("cycle") """)
	cur.execute("""INSERT INTO tags(name) VALUES("cyclelock") """)
	cur.execute("""INSERT INTO tags(name) VALUES("Bags") """)
	cur.execute("""INSERT INTO tags(name) VALUES("table") """)
	cur.execute("""INSERT INTO tags(name) VALUES("board") """)


	cur.execute("SELECT * FROM tags")
	records = cur.fetchall()
	# for rows in records:
	# 	print(rows)
	conn.commit()



		

		


