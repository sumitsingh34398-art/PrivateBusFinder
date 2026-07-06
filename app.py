from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
buses = []

@app.route("/")
def home():
    return render_template("index.html")
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
    boarding = request.form["boarding"]
    destination = request.form["destination"]
    time = request.form["time"]
    bus = request.form["bus"]
    route = boarding + " → " + destination
    
    print(boarding)
    print(destination)
    print(time)
    print(bus)
    print(route)
    
    buses.append({
        "boarding": boarding,
        "destination": destination,
        "time": time,
        "bus": bus,
        "route": route
    })
    return redirect(url_for("dashboard"))

@app.route("/search", methods=["POST"])
def search():
    
    global buses

    boarding = request.form["boarding"].strip().lower()
    destination = request.form["destination"].strip().lower()

    buses = [
        {
            "boarding":"Rampura",
            "destination":"Pilani",
            "time":"08:30 AM",
            "bus":"Billu Bus Travels",
            "route":"Rampura → Pilani"
        },
        {
            "boarding":"Rampura",
            "destination":"Pilani",
            "time":"10:00 AM",
            "bus":"Pawan Bus Travels",
            "route":"Rampura → Pilani"
        },
        {
            "boarding":"Rampura",
            "destination":"Pilani",
            "time":"11:15 AM",
            "bus":"No Name Bus Travels",
            "route":"Rampura → Pilani"
        },
        {
            "boarding":"Rampura",
            "destination":"Pilani",
            "time":"11:45 AM",
            "bus":"Mini Bus Travels",
            "route":"Rampura → Pilani"
        },
        {
            "boarding":"Rampura",
            "destination":"Pilani",
            "time":"12:45 PM",
            "bus":"Billu Bus Travels",
            "route":"Rampura → Pilani"
        },
        {
            "boarding":"Rampura",
            "destination":"Pilani",
            "time":"02:30 PM",
            "bus":"Confirm Nhi Bus Travels",
            "route":"Rampura → Pilani"
        },
        {
            "boarding":"Rampura",
            "destination":"Pilani",
            "time":"04:30 PM",
            "bus":"Billu Bus Travels",
            "route":"Rampura → Pilani"
        },
        {
            "boarding":"Rampura",
            "destination":"Bahal",
            "time":"09:00 AM",
            "bus":"Mini Bus Travels",
            "route":"Rampura → Bahal"
        },
        {
            "boarding":"Pilani",
            "destination":"Rampura",
            "time":"08:00 AM",
            "bus":"Mini Bus Travels",
            "route":"Pilani → Rampura"
        },
        {
            "boarding":"Pilani",
            "destination":"Rampura",
            "time":"10:15 AM",
            "bus":"Billu Bus Travels",
            "route":"Pilani → Rampura"
        }
    ]
    filtered_buses = []
    for bus in buses:
        if bus["boarding"].lower() == boarding and bus["destination"].lower() == destination:
            filtered_buses.append(bus)

    return render_template(
        "result.html",
        boarding=boarding,
        destination=destination,
        buses=filtered_buses
    )

if __name__ == "__main__":
    app.run(debug=True)
