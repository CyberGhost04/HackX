from flask import Flask, render_template, request, Response, send_from_directory, stream_with_context, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, auth
import google.generativeai as genai
import time
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure secret key

# Set up Google Generative AI API key
genai.configure(api_key='AIzaSyAEZ0azeHxioW6IBlBnP3niII8RpK9H_mk')  # Replace with your API key
gemini = genai.GenerativeModel()

# Initialize Firebase Admin SDK
# cred = credentials.Certificate(r"C:\Users\Shivam\Python\PPTGenerator\health-monitoring\wellness-sync-aec5f-firebase-adminsdk-iy5pb-07d2fb859c.json")
# firebase_admin.initialize_app(cred)

def clean_text(text):
    """Clean up text from Gemini responses."""
    return text.replace('\n', '<br>').replace('', '').replace('*', '')

def generate_recommendations(user_data):
    """Generate recommendations based on user data using Gemini API."""
    prompt = f"""
    Based on the user's data:
    Name: {user_data['Name']},
    Age: {user_data['Age']},
    BMI: {user_data['BMI']},
    Gender: {user_data['Gender']},
    Chronic Conditions: {user_data['Chronic Conditions']},
    Current Medications: {user_data['Current Medications']},
    Hereditary Conditions: {user_data['Hereditary Conditions']},
    Smoking: {user_data['Smoking']},
    Alcohol Consumption: {user_data['Alcohol Consumption']},
    Physical Activity: {user_data['Physical Activity']},
    Sleep Patterns: {user_data['Sleep Patterns']},
    Diet Preferences: {user_data['Diet Preferences']},
    Mental Health Status: {user_data['Mental Health Status']},
    Recent Illnesses: {user_data['Recent Illnesses']},
    Medication Adherence: {user_data['Medication Adherence']}
    
    Predict the future health issues this person might be prone to, considering their lifestyle, existing conditions, and hereditary risks. Provide personalized insights about potential health concerns over the next 5-10 years, and suggest strategies for prevention and management."
    """
    chat = gemini.start_chat(history=[])
    response = chat.send_message(prompt, stream=True)
    content_text = ""
    for chunk in response:
        content_text += chunk.text
        cleaned_text = clean_text(content_text)
    return cleaned_text

def handle_user_input(user_data):
    """Stream recommendations word by word to the client."""
    recommendations = generate_recommendations(user_data)
    words = recommendations.split()
    for word in words:
        yield f"{word}\n\n"
        time.sleep(0.1)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/baymax.jpg')
def send_image():
    return send_from_directory('static/images', 'baymax.jpg')

@app.route('/mail5.avif')
def send_second_image():
    return send_from_directory('static/images', 'mail5.avif')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'root@email' and password == 'root':
            session['user'] = 'root'
            return redirect(url_for('home'))
        else:
            flash('Email or Password is incorrect. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('Registration is disabled.')
        return redirect(url_for('login'))
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

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = round(weight / (height / 100) ** 2, 2)

        user_data = {
            'Name': request.form['name'],
            'Age': request.form['age'],
            'Weight': weight,
            'Height': height,
            'BMI': bmi,
            'Gender': request.form['gender'],
            'Chronic Conditions': request.form['chronic_conditions'],
            'Current Medications': request.form['current_medications'],
            'Hereditary Conditions': request.form['hereditary_conditions'],
            'Smoking': request.form['smoking'],
            'Alcohol Consumption': request.form['alcohol_consumption'],
            'Physical Activity': request.form['physical_activity'],
            'Sleep Patterns': request.form['sleep_patterns'],
            'Diet Preferences': request.form['diet_preferences'],
            'Mental Health Status': request.form['mental_health_status'],
            'Recent Illnesses': request.form['recent_illnesses'],
            'Medication Adherence': request.form['medication_adherence']
        }

        return Response(stream_with_context(handle_user_input(user_data)), content_type='text/event-stream')
    return render_template('survey.html')

@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)