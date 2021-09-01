from collections import namedtuple
import psycopg2
import datetime

conn = psycopg2.connect(dbname='library', user='postgres', password='1Giaape1')
curr = conn.cursor()


def find_book():
    # set search variables
    title = input('Type the title: ')
    author = input('Type the author: ')

    sql = f"""SELECT * FROM books WHERE (title LIKE '%{title}%' and author LIKE '%{author}%')"""

    # Get results from db and print matching books
    try:
        curr.execute(sql)
        if curr.rowcount != 0:
            res = curr.fetchall()
            print('Found:')
            for single in res:
                print(f'    {single[0]}.{single[1]} by {single[2]}')
        else:
            print('Unfortunately, no book matches your criteria')
            return
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    # TODO: Prevent user from typing different id than has been showed
    # Choosing exact book and returning Book class object
    while True:
        book_id = int(input('Choose one of them or press 0 to go back: '))
        if book_id == 0:
            break
        else:
            try:
                curr.execute(f"""SELECT * FROM library.public.books inner join library.public.menage on 
                books.id = book_id WHERE books.id = {book_id}""")
                res = curr.fetchone()
                book = Book(res[0], res[1], res[2], res[3])
                menage = MenageBook(res[4], res[5], res[6], res[7])
                return book, menage
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)


def add_book():
    # TODO: Write it nicer.....
    # filling in book information
    title = input('Type the title: ')
    author = input('Type the author: ')
    pages = input('Type amount of pages: ')
    sql = f"""INSERT INTO library.public.books (title, author, pages) 
    VALUES ('{title}', '{author}', {int(pages)});
    """

    # adding book to the db
    try:
        curr.execute(sql)
        curr.execute('SELECT * FROM books ORDER BY id DESC limit 1')
        men_id = curr.fetchone()[0]
        sql2 = f"""INSERT INTO library.public.menage (status, return_date, book_id) 
        VALUES ('available', NULL, {men_id});"""
        curr.execute(sql2)
        print(f'Book has been added to the database')
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


class Book(namedtuple('Book', ['id', 'title', 'author', 'pages'])):

    def __repr__(self):
        return f'Book named {self.title} written by {self.author}'

    # deletes row in books table as well as in menage table
    def delete_book(self):
        sql = f"""delete from books where id={self.id}"""
        try:
            curr.execute(sql)
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


class MenageBook:

    def __init__(self, men_id, status, date, id_fk):
        self.men_id = men_id
        self.status = status
        self.date = date
        self.id_fk = id_fk

    def return_book(self):
        if self.status == 'borrowed':
            sql = f"""update library.public.menage set status = 'available' where book_id = {self.id_fk};
            update library.public.menage set return_date = NULL where book_id = {self.id_fk}"""
            try:
                curr.execute(sql)
                conn.commit()
                print(f'Book has been returned')
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
        elif self.status == 'available':
            print('This book is not borrowed, did you meant to borrow it?(yes or no)')
            while True:
                choice = input('>>')
                if choice == 'yes':
                    self.borrow_book()
                    break
                elif choice == 'no':
                    break
                else:
                    print('You must have entered your choice incorrectly, try again')

    def borrow_book(self):
        if self.status == 'borrowed':
            print(f'This book is not currently available, come when it is returned ({self.date})')
        elif self.status == 'available':
            self.date = datetime.date.today() + datetime.timedelta(days=14)
            self.date = self.date.strftime('%Y-%m-%d')

            sql = f"""update library.public.menage set status = 'borrowed' where book_id = {self.id_fk};
                update library.public.menage set return_date = '{self.date}' where book_id = {self.id_fk};"""
            try:
                curr.execute(sql)
                conn.commit()
                print(f'Book has been borrowed, please return it {self.date}')
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)

    def prolong_book(self):
        if self.status == 'borrowed':
            self.date = datetime.date.today() + datetime.timedelta(days=14)
            sql = f"""update library.public.menage set return_date = '{self.date}' where book_id = {self.id_fk}"""
            try:
                curr.execute(sql)
                print(f'Return date has been changed, please return book before {self.date}')
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
        elif self.status == 'available':
            print("This book is not borrowed, did you meant to borrow it? (yes or no)")
            while True:
                action = input('\n>> ')
                if action == 'Yes' or 'yes':
                    self.borrow_book()
                    break
                elif action == 'No' or 'no':
                    break
                else:
                    print('You must have entered your choice incorrectly, try again')