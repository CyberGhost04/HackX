from flask import Flask, render_template, request, Response, stream_with_context, redirect, url_for, session, flash
import joblib
import pandas as pd
import re
import firebase_admin
from firebase_admin import credentials, auth
import google.generativeai as genai
import time
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure secret key

# Load the model and preprocessor
model = joblib.load('model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# Set up Google Generative AI API key
genai.configure(api_key='AIzaSyAEZ0azeHxioW6IBlBnP3niII8RpK9H_mk')  # Replace with your API key
gemini = genai.GenerativeModel()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\Shivam\Python\PPTGenerator\health-monitoring\wellness-sync-aec5f-firebase-adminsdk-iy5pb-07d2fb859c.json"
)
firebase_admin.initialize_app(cred)

def clean_text(text):
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    return text

def generate_recommendations(prediction, user_data):
    prompt = f"""
    Based on the user's data:
    Age: {user_data['Age']},
    BMI: {user_data['BMI']},
    Specific ailments: {user_data['Specific ailments']},
    Food preference: {user_data['Food preference']},
    Smoker?: {user_data['Smoker?']},
    Living in?: {user_data['Living in?']},
    Any hereditary condition?: {user_data['Any heriditary condition?']},
    Follow Diet: {user_data['Follow Diet']},
    Physical activity: {user_data['Physical activity']},
    Regular sleeping hours: {user_data['Regular sleeping hours']},
    Alcohol consumption: {user_data['Alcohol consumption']},
    Social interaction: {user_data['Social interaction']},
    Taking supplements: {user_data['Taking supplements']},
    Mental health management: {user_data['Mental health management']},
    Illness count last year: {user_data['Illness count last year']}
    
    Prediction of illness count for the next year: {prediction}
    
    Provide personalized wellness recommendations.
    """
    chat = gemini.start_chat(history=[])
    response = chat.send_message(prompt, stream=True)
    content_text = ""
    for chunk in response:
        content_text += chunk.text
        content_text = clean_text(content_text)
        content_text = content_text.replace('\n', '<br>')
    return content_text

def predict_health(user_data):
    df = pd.DataFrame([user_data])
    X_preprocessed = preprocessor.transform(df)
    prediction = model.predict(X_preprocessed)
    recommendations = generate_recommendations(prediction[0], user_data)
    return recommendations

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Check user credentials with Firebase
            user = auth.get_user_by_email(email)
            # For simplicity, assuming success here. Implement actual password check in production
            session['user'] = user.uid
            return redirect(url_for('home'))
        except Exception as e:
            flash('Email or Password is incorrect. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Create user in Firebase
            auth.create_user(email=email, password=password)
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

def handle_user_input(user_data):
    recommendations = predict_health(user_data)
    words = recommendations.split()
    for word in words:
        yield f"data: {word}\n\n"
        time.sleep(0.1)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_data = {
            'Age': request.form['age'],
            'BMI': request.form['bmi'],
            'Specific ailments': request.form['ailments'],
            'Food preference': request.form['food_preference'],
            'Smoker?': request.form['smoker'],
            'Living in?': request.form['living_in'],
            'Any heriditary condition?': request.form['hereditary_condition'],
            'Follow Diet': request.form['follow_diet'],
            'Physical activity': request.form['physical_activity'],
            'Regular sleeping hours': request.form['sleeping_hours'],
            'Alcohol consumption': request.form['alcohol_consumption'],
            'Social interaction': request.form['social_interaction'],
            'Taking supplements': request.form['supplements'],
            'Mental health management': request.form['mental_health'],
            'Illness count last year': request.form['illness_lastyear']
        }

        return Response(stream_with_context(handle_user_input(user_data)), content_type='text/event-stream')
    return render_template('survey.html')

@app.route('/recommendations')
def recommendations():
    user_data = {
        'Age': request.args.get('age'),
        'BMI': request.args.get('bmi'),
        'Specific ailments': request.args.get('ailments'),
        'Food preference': request.args.get('food_preference'),
        'Smoker?': request.args.get('smoker', 'off') == 'on',
        'Living in?': request.args.get('living_in'),
        'Any heriditary condition?': request.args.get('hereditary_condition'),
        'Follow Diet': request.args.get('follow_diet'),
        'Physical activity': request.args.get('physical_activity'),
        'Regular sleeping hours': request.args.get('sleeping_hours'),
        'Alcohol consumption': request.args.get('alcohol_consumption'),
        'Social interaction': request.args.get('social_interaction'),
        'Taking supplements': request.args.get('supplements'),
        'Mental health management': request.args.get('mental_health'),
        'Illness count last year': request.args.get('illness_lastyear')
    }
    return Response(stream_with_context(handle_user_input(user_data)), content_type='text/event-stream')
@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
