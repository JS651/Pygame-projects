import sqlite3
from tkinter import *

def add_artist():
    artist_name = artist_name_entry.get()
    address = artist_address_entry.get()
    town = artist_town_entry.get()
    county = artist_county_entry.get()
    postcode = artist_postcode_entry.get()
    cursor.execute("INSERT INTO Artists (name, address, town, county, postcode) VALUES (?, ?, ?, ?, ?)",
                   (artist_name, address, town, county, postcode))
    db.commit()
    clear_artist_entries()
    artist_name_entry.focus()

def clear_artist_entries():
    artist_name_entry.delete(0, END)
    artist_address_entry.delete(0, END)
    artist_town_entry.delete(0, END)
    artist_county_entry.delete(0, END)
    artist_postcode_entry.delete(0, END)
    artist_name_entry.focus()

def view_artists():
    cursor.execute("SELECT * FROM Artists")
    for row in cursor.fetchall():
        record = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}\n"
        output_window.insert(END, record)

def add_art():
    artist_id = art_artist_id_entry.get()
    title = art_title_entry.get()
    medium = art_medium.get()
    price = art_price_entry.get()
    cursor.execute("INSERT INTO Art (artistid, title, medium, price) VALUES (?, ?, ?, ?)",
                   (artist_id, title, medium, price))
    db.commit()
    clear_art_entries()
    artist_name_entry.focus()

def clear_art_entries():
    art_artist_id_entry.delete(0, END)
    art_title_entry.delete(0, END)
    art_medium.set("")
    art_price_entry.delete(0, END)

def clear_output():
    output_window.delete(0, END)

def search_artist():
    selected_artist = search_artist_entry.get()
    cursor.execute("SELECT name FROM Artists WHERE artistid=?", [selected_artist])
    for row in cursor.fetchall():
        output_window.insert(END, row)
        cursor.execute("SELECT * FROM Art WHERE artistid=?", [selected_artist])
        for art_row in cursor.fetchall():
            record = f"{art_row[0]}, {art_row[1]}, {art_row[2]}, {art_row[3]}, R{art_row[4]}\n"
            output_window.insert(END, record)
    search_artist_entry.delete(0, END)
    search_artist_entry.focus()

def search_by_medium():
    selected_medium = medium_search.get()
    cursor.execute("""SELECT Art.pieceid, Artists.name, Art.title, Art.medium, Art.price 
                      FROM Artists, Art 
                      WHERE Artists.artistid = Art.artistid AND Art.medium = ?""", [selected_medium])
    for row in cursor.fetchall():
        record = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, R{row[4]}\n"
        output_window.insert(END, record)
    medium_search.set("")

def search_by_price():
    min_price = min_price_entry.get()
    max_price = max_price_entry.get()
    cursor.execute("""SELECT Art.pieceid, Artists.name, Art.title, Art.medium, Art.price 
                      FROM Artists, Art 
                      WHERE Artists.artistid = Art.artistid AND Art.price >= ? AND Art.price <= ?""",
                   [min_price, max_price])
    for row in cursor.fetchall():
        record = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, R{row[4]}\n"
        output_window.insert(END, record)
    min_price_entry.delete(0, END)
    max_price_entry.delete(0, END)
    min_price_entry.focus()

def mark_as_sold():
    with open("SoldArt.txt", "a") as file:
        selected_piece = sold_piece_entry.get()
        cursor.execute("SELECT * FROM Art WHERE pieceid=?", [selected_piece])
        for row in cursor.fetchall():
            record = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}\n"
            file.write(record)
        cursor.execute("DELETE FROM Art WHERE pieceid=?", [selected_piece])
        db.commit()

def create_tables():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Artists (
                      artistid INTEGER PRIMARY KEY, 
                      name TEXT, 
                      address TEXT, 
                      town TEXT, 
                      county TEXT, 
                      postcode TEXT);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Art (
                      pieceid INTEGER PRIMARY KEY, 
                      artistid INTEGER, 
                      title TEXT, 
                      medium TEXT, 
                      price INTEGER);""")

with sqlite3.connect("Art.db") as db:
    cursor = db.cursor()
    create_tables()

window = Tk()
window.title("Art Gallery")
window.geometry("1220x600")

Label(text="Enter new details:").place(x=10, y=10, width=100, height=25)
Label(text="Name:").place(x=30, y=40, width=80, height=25)
artist_name_entry = Entry()
artist_name_entry.place(x=110, y=40, width=200, height=25)
artist_name_entry.focus()

Label(text="Address:").place(x=310, y=40, width=80, height=25)
artist_address_entry = Entry()
artist_address_entry.place(x=390, y=40, width=200, height=25)

Label(text="Town:").place(x=590, y=40, width=80, height=25)
artist_town_entry = Entry()
artist_town_entry.place(x=670, y=40, width=100, height=25)

Label(text="County:").place(x=770, y=40, width=80, height=25)
artist_county_entry = Entry()
artist_county_entry.place(x=850, y=40, width=100, height=25)

Label(text="Postcode:").place(x=950, y=40, width=80, height=25)
artist_postcode_entry = Entry()
artist_postcode_entry.place(x=1030, y=40, width=100, height=25)

Button(text="Add Artist", command=add_artist).place(x=110, y=80, width=130, height=25)
Button(text="Clear Artist", command=clear_artist_entries).place(x=250, y=80, width=130, height=25)

Label(text="Artist ID:").place(x=30, y=120, width=80, height=25)
art_artist_id_entry = Entry()
art_artist_id_entry.place(x=110, y=120, width=50, height=25)

Label(text="Title:").place(x=200, y=120, width=80, height=25)
art_title_entry = Entry()
art_title_entry.place(x=280, y=120, width=280, height=25)

Label(text="Medium:").place(x=590, y=120, width=80, height=25)
art_medium = StringVar(window)
OptionMenu(window, art_medium, "Oil", "Watercolour", "Ink", "Acrylic").place(x=670, y=120, width=100, height=25)

Label(text="Price:").place(x=770, y=120, width=80, height=25)
art_price_entry = Entry()
art_price_entry.place(x=850, y=120, width=100, height=25)

Button(text="Add Piece", command=add_art).place(x=110, y=150, width=130, height=25)
Button(text="Clear Piece", command=clear_art_entries).place(x=250, y=150, width=130, height=25)

output_window = Listbox()
output_window.place(x=10, y=200, width=1000, height=350)

Button(text="Clear Output", command=clear_output).place(x=1020, y=200, width=155, height=25)
Button(text="View All Artists", command=view_artists).place(x=1020, y=230, width=155, height=25)

Label(text="Artist ID:").place(x=1020, y=300, width=50, height=25)
search_artist_entry = Entry()
search_artist_entry.place(x=1075, y=300, width=100, height=25)
Button(text="Search by Artist", command=search_artist).place(x=1020, y=330, width=155, height=25)

Label(text="Medium:").place(x=1020, y=360, width=100, height=25)
medium_search = StringVar(window)
OptionMenu(window, medium_search, "Oil", "Watercolour", "Ink", "Acrylic").place(x=1125, y=360, width=100, height=25)
Button(text="Search", command=search_by_medium).place(x=1125, y=390, width=100, height=25)

Label(text="Min:").place(x=1020, y=420, width=50, height=25)
min_price_entry = Entry()
min_price_entry.place(x=1075, y=420, width=75, height=25)

Label(text="Max:").place(x=1150, y=420, width=50, height=25)
max_price_entry = Entry()
max_price_entry.place(x=1205, y=420, width=75, height=25)
Button(text="Search by Price", command=search_by_price).place(x=1020, y=450, width=155, height=25)

Label(text="Sold Piece ID:").place(x=1020, y=480, width=100, height=25)
sold_piece_entry = Entry()
sold_piece_entry.place(x=1125, y=480, width=75, height=25)
Button(text="Sold", command=mark_as_sold).place(x=1020, y=510, width=155, height=25)

window.mainloop()
db.close()
