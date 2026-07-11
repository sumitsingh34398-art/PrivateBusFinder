from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# डेटाबेस कनेक्शन के लिए फंक्शन
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ऑटोमैटिक डेटाबेस सेटअप (टेबल और डिफ़ॉल्ट डेटा)
def init_db_automatically():
    conn = get_db_connection()
    cursor = conn.cursor()
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
    
    # चेक करें कि डेटाबेस खाली है या नहीं
    cursor.execute("SELECT COUNT(*) FROM buses")
    if cursor.fetchone()[0] == 0:
        default_buses = [
            ("Rampura", "Pilani", "Billu Bus Travels", "08:30 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
            ("Rampura", "Pilani", "Pawan Bus Travels", "10:00 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
            
        ]
        cursor.executemany("INSERT INTO buses (boarding, destination, bus_name, departure_time, route) VALUES (?, ?, ?, ?, ?)", default_buses)
        conn.commit()
    conn.close()

init_db_automatically()

# --- USER URL ROUTES ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/timetable')
def timetable():
    return render_template('timetable.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/search", methods=["POST"])
def search():
    boarding = request.form["boarding"].strip()
    destination = request.form["destination"].strip()
    conn = get_db_connection()
    filtered_buses = conn.execute("SELECT * FROM buses WHERE boarding LIKE ? AND destination LIKE ?", 
                                  (f"%{boarding}%", f"%{destination}%")).fetchall()
    conn.close()
    return render_template("result.html", filtered_buses=filtered_buses, boarding=boarding, destination=destination)

@app.route("/route/<int:bus_id>")
def route_details(bus_id):
    conn = get_db_connection()
    bus = conn.execute("SELECT * FROM buses WHERE id = ?", (bus_id,)).fetchone()
    conn.close()
    if bus is None: return "Bus Route Not Found!", 404
    return render_template("route.html", bus=bus)

# --- ADMIN URL ROUTES ---

@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin-login", methods=["POST"])
def admin_login():
    if request.form["username"] == "admin" and request.form["password"] == "1234":
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
    conn = get_db_connection()
    conn.execute("INSERT INTO buses (boarding, destination, bus_name, departure_time, route) VALUES (?, ?, ?, ?, ?)",
                 (request.form["boarding"].strip(), request.form["destination"].strip(), request.form["bus"].strip(), request.form["time"].strip(), request.form["route"].strip()))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/view-buses")
def view_buses():
    conn = get_db_connection()
    all_buses = conn.execute("SELECT * FROM buses").fetchall()
    conn.close()
    return render_template("view_buses.html", buses=all_buses)

# 🌟 डिलीट करने वाला रूट (Complete)
@app.route("/delete-bus/<int:bus_id>")
def delete_bus(bus_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM buses WHERE id = ?", (bus_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_buses"))

@app.route("/logout")
def logout():
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# डेटाबेस कनेक्शन के लिए फंक्शन
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ऑटोमैटिक डेटाबेस सेटअप (टेबल और डिफ़ॉल्ट डेटा)
def init_db_automatically():
    conn = get_db_connection()
    cursor = conn.cursor()
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
    
    # चेक करें कि डेटाबेस खाली है या नहीं
    cursor.execute("SELECT COUNT(*) FROM buses")
    if cursor.fetchone()[0] == 0:
        default_buses = [
            ("Rampura", "Pilani", "Billu Bus Travels", "08:30 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani"),
            ("Rampura", "Pilani", "Pawan Bus Travels", "10:00 AM", "Rampura → Beri → Bangothari → Hemeenpur → Bishanpura → Pilani")
        ]
        cursor.executemany("INSERT INTO buses (boarding, destination, bus_name, departure_time, route) VALUES (?, ?, ?, ?, ?)", default_buses)
        conn.commit()
    conn.close()

init_db_automatically()

# --- USER URL ROUTES ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    boarding = request.form["boarding"].strip()
    destination = request.form["destination"].strip()
    conn = get_db_connection()
    filtered_buses = conn.execute("SELECT * FROM buses WHERE boarding LIKE ? AND destination LIKE ?", 
                                  (f"%{boarding}%", f"%{destination}%")).fetchall()
    conn.close()
    return render_template("result.html", filtered_buses=filtered_buses, boarding=boarding, destination=destination)

@app.route("/route/<int:bus_id>")
def route_details(bus_id):
    conn = get_db_connection()
    bus = conn.execute("SELECT * FROM buses WHERE id = ?", (bus_id,)).fetchone()
    conn.close()
    if bus is None: return "Bus Route Not Found!", 404
    return render_template("route.html", bus=bus)

# --- ADMIN URL ROUTES ---

@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin-login", methods=["POST"])
def admin_login():
    if request.form["username"] == "admin" and request.form["password"] == "1234":
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
    conn = get_db_connection()
    conn.execute("INSERT INTO buses (boarding, destination, bus_name, departure_time, route) VALUES (?, ?, ?, ?, ?)",
                 (request.form["boarding"].strip(), request.form["destination"].strip(), request.form["bus"].strip(), request.form["time"].strip(), request.form["route"].strip()))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/view-buses")
def view_buses():
    conn = get_db_connection()
    all_buses = conn.execute("SELECT * FROM buses").fetchall()
    conn.close()
    return render_template("view_buses.html", buses=all_buses)

# 🌟 डिलीट करने वाला रूट (Complete)
@app.route("/delete-bus/<int:bus_id>")
def delete_bus(bus_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM buses WHERE id = ?", (bus_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_buses"))

@app.route("/logout")
def logout():
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)