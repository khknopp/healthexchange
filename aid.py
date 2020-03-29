import sqlite3
from datetime import date

def create_aid(username,title,message):
	date_now=date.today()
	db=sqlite3.connect("healthexchange.db")
	cursor = db.cursor()
	cursor.execute("SELECT desc FROM users WHERE name=(?)", (username,))
	hospital=cursor.fetchone()[0]
	cursor.execute("SELECT mail FROM users WHERE name=(?)", (username,))
	mail=cursor.fetchone()[0]
	cursor.execute("SELECT phone FROM users WHERE name=(?)", (username,))
	phone=cursor.fetchone()[0]
	cursor.execute("SELECT country FROM users WHERE name=(?)", (username,))
	country=cursor.fetchone()[0]
	cursor.execute("SELECT city FROM users WHERE name=(?)", (username,))
	city=cursor.fetchone()[0]
	cursor.execute('''INSERT INTO aid(hospital,message,mail,phone,country,city,date,title) VALUES(?,?,?,?,?,?,?,?)''', (hospital,message,mail,phone,country,city,date_now,title))
	db.commit()
	db.close()

def create_info(username,title,message):
	date_now=date.today()
	db=sqlite3.connect("healthexchange.db")
	cursor = db.cursor()
	cursor.execute("SELECT desc FROM users WHERE name=(?)", (username,))
	hospital=cursor.fetchone()[0]
	cursor.execute("SELECT mail FROM users WHERE name=(?)", (username,))
	mail=cursor.fetchone()[0]
	cursor.execute("SELECT phone FROM users WHERE name=(?)", (username,))
	phone=cursor.fetchone()[0]
	cursor.execute("SELECT country FROM users WHERE name=(?)", (username,))
	cursor.execute('''INSERT INTO info(hospital,message,mail,phone,date,title) VALUES(?,?,?,?,?,?)''', (hospital,message,mail,phone,date_now,title))
	db.commit()
	db.close()

def get_aid(username):
	list=[]
	arr=[]
	db=sqlite3.connect("healthexchange.db")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM aid")
	tab=cursor.fetchall()
	cursor.execute("SELECT country FROM users WHERE name=(?)", (username,))
	country=cursor.fetchone()[0]
	for i in tab:
		if(i[3]==str(country)):
			list.append(i)
	for x in reversed(list):
		arr.append(x)
	db.commit()
	db.close()
	return arr

def get_info(username):
		list=[]
		arr=[]
		db=sqlite3.connect("healthexchange.db")
		cursor = db.cursor()
		cursor.execute("SELECT * FROM info")
		tab=cursor.fetchall()
		for i in tab:
			list.append(i)
		for x in reversed(list):
			arr.append(x)
		db.commit()
		db.close()
		return arr
