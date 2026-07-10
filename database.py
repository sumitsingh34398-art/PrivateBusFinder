import sqlite3

# 1. डेटाबेस कनेक्शन और टेबल बनाना
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

# 2. आपका बिल्कुल सही डेटा (तीर के निशान के साथ)
data = [
    ("Rampura", "Pilani", "Billu Bus Travels", "08:30 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
    ("Rampura", "Pilani", "Pawan Bus Travels", "10:00 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
    ("Rampura", "Pilani", "No Name Bus Travels", "11:15 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
    ("Rampura", "Pilani", "Mini Bus Travels", "11:45 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
    ("Rampura", "Pilani", "Billu Bus Travels", "12:45 PM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
    ("Rampura", "Pilani", "Confirm Nhi Bus Travels", "02:30 PM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
    ("Rampura", "Pilani", "Billu Bus Travels", "04:30 PM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
    
    # 🌟 यहाँ ध्यान दें: '->' को बदलकर ' → ' (स्पेस के साथ तीर) कर दिया गया है ताकि बॉक्स सही बनें
    ("Rampura", "Bahal", "Mini Bus Travels", "09:00 AM", "Rampura → Gugalwa → Sorda Jadid → Sorda Kadim → Bahal"),
    
    ("Pilani", "Rampura", "Mini Bus Travels", "08:00 AM", "Pilani → Bishanpura → Hemeenpur → Bangothari → Beri → Rampura"),
    ("Pilani", "Rampura", "Billu Bus Travels", "10:15 AM", "Pilani → Bishanpura → Hemeenpur → Bangothari → Beri → Rampura")
]

# पुराना साफ करके नया डालने के लिए
cursor.execute("SELECT COUNT(*) FROM buses")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO buses (boarding, destination, bus_name, departure_time, route)
    VALUES (?, ?, ?, ?, ?)
    """, data)
    conn.commit()

conn.close()
print("Database Ready!")
