from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# डेटाबेस कनेक्शन के लिए फंक्शन
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ऑटोमैटिक डेटाबेस सेटअप (टेबल और असली डिफ़ॉल्ट डेटा लोड करने के लिए)
def init_db_automatically():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. बसों के लिए टेबल बनाना
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        boarding TEXT,
        destination TEXT,
        bus_name TEXT,
        departure_time TEXT,
        route TEXT
    )
    """)
    
    # 2. बीच के गाँवों (Exact Values) के साथ डिफ़ॉल्ट डेटा
    default_buses = [
        ("Rampura", "Pilani", "Billu Bus Travels", "08:30 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
        ("Rampura", "Pilani", "Pawan Bus Travels", "10:00 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
        ("Rampura", "Pilani", "No Name Bus Travels", "11:15 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
        ("Rampura", "Pilani", "Mini Bus Travels", "11:45 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
        ("Rampura", "Pilani", "Billu Bus Travels", "12:45 PM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
        ("Rampura", "Pilani", "Confirm Nhi Bus Travels", "02:30 PM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
        ("Rampura", "Pilani", "Billu Bus Travels", "04:30 PM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
        
        # रामपुर से बहल के बीच के सारे असली गाँव तीर (→) के साथ
        ("Rampura", "Bahal", "Mini Bus Travels", "09:00 AM", "Rampura → Gugalwa → Sorda Jadid → Sorda Kadim → Bahal"),
        
        ("Pilani", "Rampura", "Mini Bus Travels", "08:00 AM", "Pilani → Bishanpura → Hemeenpur → Bangothari → Beri → Rampura"),
        ("Pilani", "Rampura", "Billu Bus Travels", "10:15 AM", "Pilani → Bishanpura → Hemeenpur → Bangothari → Beri → Rampura")
    ]
    
    # चेक करना कि डेटा खाली है या नहीं, ताकि बार-बार डुप्लिकेट न हो
    cursor.execute("SELECT COUNT(*) FROM buses")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO buses (boarding, destination, bus_name, departure_time, route)
        VALUES (?, ?, ?, ?, ?)
        """, default_buses)
        conn.commit()
        print("🎉 सभी बसें और बीच के गाँव डेटाबेस में लोड हो चुके हैं!")
        
    conn.close()

# ऐप चालू होते ही डेटाबेस को सिंक करें
init_db_automatically()


# --- URL ROUTES ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/timetable")
def timetable():
    return render_template("timetable.html")
    
@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin-login", methods=["POST"])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "1234":
        return redirect(url_for("dashboard"))
    return "Invalid Username or Password"

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/add-bus")
def add_bus():
    return render_template("add_bus.html")

@app.route("/save-bus", methods=["POST"])
def save_bus():
    boarding = request.form["boarding"].strip()
    destination = request.form["destination"].strip()
    time = request.form["time"].strip()
    bus_name = request.form["bus"].strip()
    route = request.form["route"].strip()
    
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO buses (boarding, destination, bus_name, departure_time, route)
        VALUES (?, ?, ?, ?, ?)
    """, (boarding, destination, bus_name, time, route))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/search", methods=["POST"])
def search():
    boarding = request.form["boarding"].strip()
    destination = request.form["destination"].strip()

    conn = get_db_connection()
    # LIKE ऑपरेटर ताकि छोटा-बड़ा अक्षर (Case Insensitive) सब मैच हो जाए
    filtered_buses = conn.execute("""
        SELECT * FROM buses 
        WHERE boarding LIKE ? AND destination LIKE ?
    """, (f"%{boarding}%", f"%{destination}%")).fetchall()
    conn.close()

    return render_template(
        "result.html",
        filtered_buses=filtered_buses,
        boarding=boarding,
        destination=destination
    )

@app.route("/route/<int:bus_id>")
def route_details(bus_id):
    conn = get_db_connection()
    bus = conn.execute("SELECT * FROM buses WHERE id = ?", (bus_id,)).fetchone()
    conn.close()
    
    if bus is None:
        return "Bus Route Not Found!", 404
        
    return render_template("route.html", bus=bus)

if __name__ == "__main__":
    app.run(debug=True)
