import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS buses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    boarding TEXT,
    destination TEXT,
    bus_name TEXT,
    departure_time TEXT,
    route TEXT
)
""")

data = [
("Rampura","Pilani","Billu Bus Travels","08:30 AM","Rampura → Pilani"),
("Rampura","Pilani","Pawan Bus Travels","10:00 AM","Rampura → Pilani"),
("Rampura","Pilani","No Name Bus Travels","11:15 AM","Rampura → Pilani"),
("Rampura","Pilani","Mini Bus Travels","11:45 AM","Rampura → Pilani"),
("Rampura","Pilani","Billu Bus Travels","12:45 PM","Rampura → Pilani"),
("Rampura","Pilani","Confirm Nhi Bus Travels","02:30 PM","Rampura → Pilani"),
("Rampura","Pilani","Billu Bus Travels","04:30 PM","Rampura → Pilani"),
("Rampura","Bahal","Mini Bus Travels","09:00 AM","Rampura → Bahal"),
("Pilani","Rampura","Mini Bus Travels","08:00 AM","Pilani → Rampura"),
("Pilani","Rampura","Billu Bus Travels","10:15 AM","Pilani → Rampura")
]

cursor.executemany("""
INSERT INTO buses
(boarding,destination,bus_name,departure_time,route)
VALUES (?,?,?,?,?)
""", data)

conn.commit()
conn.close()

print("Database Ready!")