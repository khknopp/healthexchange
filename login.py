import hashlib, os, binascii, sqlite3

def hash(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),salt.encode('ascii'),100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def createdb():
    db = sqlite3.connect("healthexchange.db")
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(name TEXT,password TEXT,desc TEXT,mail TEXT,phone TEXT, country TEXT, city TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS help(desc TEXT,mail TEXT,phone TEXT, country TEXT,message TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS info(desc TEXT,mail TEXT,phone TEXT, country TEXT,message TEXT)''')
    db.commit()
    db.close()

def insertuser(username, hash,desc,mail,phone,country,city):
    db = sqlite3.connect("healthexchange.db")
    cursor = db.cursor()
    cursor.execute('''INSERT INTO users(name,password,desc,mail,phone,country,city) VALUES(?,?,?,?,?,?,?)''', (username,hash,desc,mail,phone,country,city))
    db.commit()
    db.close()

def signup_f(user, passwd, desc, mail, phone,country,city):
    try:
        passwdhash=hash(passwd)
        createdb()
        insertuser(user,passwdhash,desc,mail,phone,country,city)
    except:
        return False
    return True

def login_f(user, passwd):
    if passwd == "":
        return False
    db = sqlite3.connect("healthexchange.db")
    cursor = db.cursor()
    cursor.execute('''SELECT password FROM users WHERE name=?''', (user,))
    users = cursor.fetchone()
    if users == None:
        return False
    user1=users[0]
    db.commit()
    db.close()
    return verify(user1, passwd)
