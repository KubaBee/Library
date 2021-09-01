from tkinter import *
from PIL import ImageTk, Image
import BookModel
import psycopg2
import time


conn = psycopg2.connect(dbname='library', user='postgres', password='1Giaape1')
curr = conn.cursor()


while True:
    action = input("""\nSelect an action:\n1.Borrow Book\n2.Return Book\n3.Donate Book
4.Report Missing\n5.Prolong\n6.Exit\n>> """)

    if action in {'1', '2', '4', '5'}:
        try:
            current_book, menage = BookModel.find_book()
        except TypeError:
            time.sleep(2)
            continue
        except:
            print(Exception)

    if action == '1':
        menage.borrow_book()
    elif action == '2':
        menage.return_book()
    elif action == '3':
        BookModel.add_book()
    elif action == '4':
        current_book.delete_book()
        print("Book has been removed from database in return donate some book")
        BookModel.add_book()
    elif action == '5':
        menage.prolong_book()
    elif action == '6':
        break
    else:
        print('You must have entered something incorrectly, please try again')
    time.sleep(2)


curr.close()
conn.close()
# root = Tk()
#
# bg_btn = '#d9b35b'
#
# root.title("Library")
# root.geometry("490x490")
# bg_img = ImageTk.PhotoImage(Image.open("lib.png"))
# l = Label(image=bg_img)
# l.place(x=0, y=0, relwidth=1, relheight=1)
# Button(root, bg=bg_btn, text='Borrow a Book', pady=20, padx=20).grid(row=5, column=0)
# Button(root, bg=bg_btn, text='Return the Book', pady=20, padx=20).grid(row=6, column=0)
# Button(root, bg=bg_btn, text='View Books', pady=20, padx=20).grid(row=7, column=0)
# Button(root, bg=bg_btn, text='Prolong', pady=20, padx=20).grid(row=8, column=0)
#
# root.mainloop()

