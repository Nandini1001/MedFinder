# MedFinder
PUNS-medfinder is a web-based application designed to help users find medicines and their cheaper alternatives easily. This project is built using Flask (Python), and it provides a user-friendly interface to search medicines based on their names or active ingredients.

# Features
- Search medicines by name.
- Display cheaper alternatives for a medicine.
- Search results appear over a full-screen background for better visual appeal.
- User authentication: login system to access the search page.
- Responsive and simple user interface.

# Usage
- Register or login as a user.
- Enter the medicine name in the search bar.
- View the list of cheaper alternatives displayed above the full-screen background image.

# Technologies Used
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Database: CSV files for medicine data

# Project Structure
```
PUNS-medfinder/
│
├─ app.py                 # Main Flask application
├─ requirements.txt       # Python dependencies
├─ templates/             # HTML templates
│   ├─ login.html
│   ├─ find.html
|   ├─ about.html
│   └─ index.html
|    
├─ static/                # CSS, JS, and images
│   ├─ style.css/
│   ├─ js/
│   |   ├─ allergy.js
|   |   └─ script.js 
|   └─ images/
|        ├─ bg.jpg
│        ├─ bg_find.png
|        ├─ logo.jpg
│        └─ bg_signup.jpeg
├─ grouped_allergies_medicines_salts_CORRECTED.csv          # Medicine data
├─ hashed_med+allergy_separated.csv                         # Medicine data
└─ README.md              # Project documentation
```
# Steps to Create serviceAccountKey.json from Firebase
- Go to Firebase Console
- Select the project you want to use.
- Click the gear icon next to “Project Overview”.
- Choose Project Settings.
- In the top menu, click on Service accounts.
- Click Generate new private key.
- A pop-up will appear; click Generate key.
- Firebase will automatically download a JSON file to your computer. This is your serviceAccountKey.json.
