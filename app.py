from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from google.cloud import firestore
from flask_cors import CORS
import os
import csv
from collections import defaultdict
import heapq

# Set path to Google Cloud service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
CORS(app)

# Firestore client
db = firestore.Client()

class CheapMedicine:
    def __init__(self, name, salt, price, unit_size):
        self.name = name
        self.salt = salt
        self.price = float(price)
        self.unit_size = unit_size

    def __lt__(self, other):
        return self.price < other.price

def to_lower(s):
    return s.lower()

def split(s, delimiter):
    return s.split(delimiter)

def load_allergy_data(filename):
    allergy_map = defaultdict(set)
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            allergy = to_lower(row[0])
            meds = split(row[1], '|')
            for med in meds:
                allergy_map[allergy].add(to_lower(med))
    return allergy_map

def load_medicine_data(filename):
    med_data = []
    with open(filename, newline='', encoding='utf-8') as med_file:
        reader = csv.reader(med_file)
        next(reader)
        for row in reader:
            if row:
                med_data.append(row)
    return med_data

def search_medicine(medicine_name, allergies, allergy_map, med_data):
    results = []
    warnings = []
    allergies = [to_lower(a.strip()) for a in allergies if a.strip()]
    medicine_name = to_lower(medicine_name)

    for row in med_data:
        if len(row) < 11:
            continue
        med_name = row[1]
        med_name_lower = to_lower(med_name)
        if medicine_name in med_name_lower:
            excluded = any(med_name_lower in allergy_map.get(allergy, set()) for allergy in allergies if allergy != "none")
            if excluded:
                warnings.append(f"'{med_name}' is a possible match but was excluded due to selected allergies.")
                continue

            med_info = {
                "name": row[1],
                "unit": row[2],
                "price": row[3],
                "salts": row[6],
                "effects": row[16] if len(row) > 16 else "Not available",
                "alternatives": []
            }

            cheap_names = split(row[7], '|')
            cheap_salts = split(row[8], '|')
            cheap_prices = split(row[9], '|')
            cheap_units = split(row[10], '|')

            cheap_list = []
            for i in range(len(cheap_names)):
                try:
                    cm = CheapMedicine(cheap_names[i], cheap_salts[i], cheap_prices[i], cheap_units[i])
                    heapq.heappush(cheap_list, cm)
                except Exception:
                    continue

            while cheap_list:
                c = heapq.heappop(cheap_list)
                med_info["alternatives"].append({
                    "name": c.name,
                    "salts": c.salt,
                    "price": c.price,
                    "unit_size": c.unit_size
                })

            results.append(med_info)

    return results, warnings

# Load once
allergy_map = load_allergy_data("grouped_allergies_medicines_salts_CORRECTED.csv")
med_data = load_medicine_data("hashed_med+allergy_separated.csv")

allergy_list = [
    "Allergic rash risk", "Allergic reaction risk", "Allergy risk(injection site)",
    "Cephalosphorin allergy", "Liver toxicity and allergy risk", "NSAID allergy",
    "Penicillin allergy", "Stevens johnson syndrome", "Sulfa allergy",
    "Sulpha allergy with combination", "Tetracycline allergy", "Topical allergy risk"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        db.collection('users').document(email).set({
            'fullname': fullname,
            'email': email,
            'password': password  # 🔒 You should hash passwords in production
        })
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        user_doc = db.collection('users').document(email).get()
        if user_doc.exists and user_doc.to_dict()['password'] == password:
            session['user'] = {
                'uid': email,
                'email': email,
                'name': user_doc.to_dict().get('fullname', 'No Name'),
                'is_guest': False
            }
            return redirect(url_for('find'))
        else:
            return "Invalid credentials."

    return render_template('login.html')

@app.route('/firebase-login', methods=['POST'])
def firebase_login():
    data = request.get_json()
    session['user'] = {
        'uid': data['uid'],
        'email': data['email'],
        'name': data['name'],
        'is_guest': data['is_guest']
    }
    return jsonify({ 'message': 'User session stored successfully' }), 200

@app.route('/guest-login', methods=['POST'])
def guest_login():
    session['user'] = {
        'uid': 'guest',
        'email': 'guest@guest.com',
        'name': 'Guest User',
        'is_guest': True
    }
    return redirect(url_for('find'))

@app.route('/home')
def home():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template("home.html", user=user)

'''@app.route('/find',methods=['GET', 'POST'])
def find():
    return render_template('find.html')'''
@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        medicine = request.form.get('medicine', '')
        allergies = request.form.getlist('allergies')
        results, warnings = search_medicine(medicine, allergies, allergy_map, med_data)
        return render_template('find.html', results=results, warnings=warnings, allergy_list=allergy_list)
    return render_template('find.html', results=None, warnings=None, allergy_list=allergy_list)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)