# Vehicle-IQ 

**AI-Based Used Vehicle Price Prediction System**

Vehicle-IQ is a Flask web application that predicts the market price of a used vehicle based on its features. It was built as a group project during Year 2, Semester 2 of our BSc (Hons) in Information Technology at SLIIT.

---

## What It Does

Used vehicle pricing in Sri Lanka is inconsistent — the same car listed by two different sellers can have a price gap of hundreds of thousands of rupees. Vehicle-IQ gives buyers and sellers a data-driven price estimate based on the actual features of the vehicle, making negotiations fairer and more informed.

Users enter details about a vehicle and the system returns a predicted price using a trained machine learning model.

---

## Features

- **Price Prediction** — Enter vehicle details and get an instant ML-based price estimate
- **User Authentication** — Register and log in securely (Flask-Login + Flask-Bcrypt)
- **Prediction History** — Every prediction is saved to your account so you can track and compare
- **Feedback System** — Flag predictions that seem off so the system can be improved
- **Admin Dashboard** — Admins can manage users, view all predictions, and review feedback

---

## Input Features Used for Prediction

| Feature | Example |
|---|---|
| Vehicle Model | Toyota Aqua, Honda Vezel |
| Model Year | 2018 |
| Mileage | 45,000 km |
| Transmission | Automatic / Manual |
| Fuel Type | Petrol / Hybrid / Diesel |
| Engine Capacity | 1500 cc |
| Condition | Good / Fair / Excellent |
| Location | Colombo / Kandy / Gampaha |
| Colour | White / Black / Silver |
| Vehicle Type | Car / Van / SUV |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML | Scikit-learn, Pandas, Pickle |
| Database | SQLite, Flask-SQLAlchemy |
| Auth | Flask-Login, Flask-Bcrypt, Flask-WTF |
| Frontend | HTML, CSS, Jinja2 Templates |
| Notebook | Jupyter Notebook (model training) |

---

## Project Structure

```
Vehicle-IQ-main/
│
├── app.py                  # Main Flask application
├── models.py               # Database models (User, Prediction, Feedback)
├── forms.py                # WTForms for input validation
│
├── templates/              # HTML templates (Jinja2)
│   ├── index.html
│   ├── predict.html
│   ├── history.html
│   ├── admin.html
│   └── ...
│
├── static/                 # CSS, images
│
├── model/                  # Serialized ML model and encoders (.pkl files)
│
└── notebook/               # Jupyter notebook used for model training
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/seyawidumini/Vehicle-IQ.git
cd Vehicle-IQ/Vehicle-IQ-main

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## How the ML Model Works

1. The model was trained on a dataset of Sri Lankan used vehicle listings
2. Categorical features (fuel type, transmission, location, etc.) were encoded using label/ordinal encoding
3. A regression model was trained and serialized using Pickle
4. On each prediction request, user input is processed with Pandas and passed through the same encoding pipeline before the model generates a price estimate

The Jupyter notebook in `/notebook` covers the full training process — data cleaning, feature engineering, model selection, and evaluation.

---

## Group Project

This was a collaborative academic project. Contributions covered model development, backend development, frontend design, database design, and testing.

---

## License

This project was built for academic purposes at SLIIT. Not licensed for commercial use.
