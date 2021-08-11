import os, sqlite3
os.chdir(__file__.replace(os.path.basename(__file__), ''))

sql = sqlite3.connect('library.db')
db = sql.cursor()

def rebuildDB():
    try:    
        db.execute("DROP TABLE books")
    except:
        pass
    try:    
        db.execute("DROP TABLE authors")
    except:
        pass
    try:    
        db.execute("DROP TABLE genres")
    except:
        pass

    db.execute("""CREATE TABLE authors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
                )""")

    db.execute("""CREATE TABLE genres(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
                )""")

    db.execute("""CREATE TABLE books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                author_id INT REFERENCES authors(id),
                genre_id INT REFERENCES genres(id),
                shelf CHAR(2),
                borrow TEXT
                )""")
    sql.commit()
def resetDB():
    db.execute("DELETE FROM books")
    db.execute("DELETE FROM authors")
    db.execute("DELETE FROM genres")
    sql.commit()

def addAuthor(name):
    db.execute('INSERT INTO authors(name) VALUES(?)', (name,))
    sql.commit()
def addGenre(name):
    db.execute('INSERT INTO genres(name) VALUES(?)', (name,))
    sql.commit()
def newBook(name, author, genre, shelf):
    db.execute(f'SELECT id FROM authors WHERE name LIKE "{author}"')
    a = db.fetchone()
    if a == None:
        addAuthor(author)
        newBook(name, author, genre, shelf)
        return
    db.execute(f'SELECT id FROM genres WHERE name LIKE "{genre}"')
    g = db.fetchone()
    if g == None:
        addGenre(genre)
        newBook(name, author, genre, shelf)
        return
    db.execute('''INSERT INTO books(name, author_id, genre_id, shelf, borrow) 
                VALUES(?, ?, ?, ?, "NONE")''', (name, a[0], g[0], shelf))
    sql.commit()

def deleteBook(name):
    db.execute('DELETE FROM books WHERE name = ?', (name,))
    sql.commit()

def searchByName(name):
    db.execute('SELECT name, author_id, genre_id, shelf, borrow FROM books WHERE name LIKE ?', ('%'+name+'%',))
    return db.fetchall()
def searchByAuthor(author):
    db.execute('SELECT name, author_id, genre_id, shelf, borrow FROM books WHERE author_id = (SELECT id FROM authors WHERE name LIKE ?)', ('%'+author+'%',))
    return db.fetchall()
def searchByGenre(genre):
    db.execute('SELECT name, author_id, genre_id, shelf, borrow FROM books WHERE genre_id = (SELECT id FROM genres WHERE name LIKE ?)', ('%'+genre+'%',))
    return db.fetchall()

def author(id):
    db.execute('SELECT name FROM authors WHERE id = ?', (id,))
    try :
        return db.fetchone()[0]
    except:
        return 0
def genre(id):
    db.execute('SELECT name FROM genres WHERE id = ?', (id,))
    try:
        return db.fetchone()[0]
    except:
        return 0

def borrowBook(book, person):
    db.execute('UPDATE books SET borrow = ? WHERE name = ?', (person, book))
    sql.commit()
def returnBook(book):
    db.execute('UPDATE books SET borrow = "NONE" WHERE name = ?', (book,))
    sql.commit()

if __name__ == '__main__':
    # i = input("DO YOU WANT TO RESET THE DATABASE TO ORIGINAL STATE? ").upper()
    # if i == 'Y' or i == 'YES':
    #     import json
    #     rebuildDB()
    #     with open("example.json") as file:
    #         data = json.load(file)
    #         for book in data['Books']:
    #             newBook(book[0], book[1], book[2], '1A')
    exit()