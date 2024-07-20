import re
import pandas as pd
import joblib
import gradio as gr
import google.generativeai as genai
from flask import Flask
import time

app = Flask(__name__)

# Load the model and preprocessor
model = joblib.load('model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# Set up Google Generative AI API key
genai.configure(api_key='AIzaSyAEZ0azeHxioW6IBlBnP3niII8RpK9H_mk')
gemini = genai.GenerativeModel()

def generate_recommendations(prediction, user_data):
    prompt = f"""
    Based on the user's data:
    Age: {user_data['Age']},
    BMI: {user_data['BMI']},
    Specific ailments: {user_data['Specific ailments']},
    Food preference: {user_data['Food preference']},
    Smoker: {user_data['Smoker?']},
    Living in: {user_data['Living in?']},
    Any heriditary condition: {user_data['Any heriditary condition?']},
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
        content_text = content_text.replace("**", "").replace("*", "").replace('\n', '<br>')
    return content_text

def predict_health(age, bmi, ailments, food_preference, smoker, living_in, heriditary_condition, follow_diet, physical_activity, sleeping_hours, alcohol_consumption, social_interaction, supplements, mental_health, illness_lastyear):
    user_data = {
        'Age': age,
        'BMI': bmi,
        'Specific ailments': ailments,
        'Food preference': food_preference,
        'Smoker?': smoker,
        'Living in?': living_in,
        'Any heriditary condition?': heriditary_condition,
        'Follow Diet': follow_diet,
        'Physical activity': physical_activity,
        'Regular sleeping hours': sleeping_hours,
        'Alcohol consumption': alcohol_consumption,
        'Social interaction': social_interaction,
        'Taking supplements': supplements,
        'Mental health management': mental_health,
        'Illness count last year': illness_lastyear
    }

    df = pd.DataFrame([user_data])
    X_preprocessed = preprocessor.transform(df)
    prediction = model.predict(X_preprocessed)
    recommendations = generate_recommendations(prediction[0], user_data)
    return recommendations

def handle_user_input(age, bmi, ailments, food_preference, smoker, living_in, heriditary_condition, follow_diet, physical_activity, sleeping_hours, alcohol_consumption, social_interaction, supplements, mental_health, illness_lastyear):
    recommendations = predict_health(age, bmi, ailments, food_preference, smoker, living_in, heriditary_condition, follow_diet, physical_activity, sleeping_hours, alcohol_consumption, social_interaction, supplements, mental_health, illness_lastyear)
    
    content = ""
    words = recommendations.split()
    for word in words:
        content += word + " "
        yield gr.update(value=content)
        time.sleep(0.1)

def display_form():
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

def display_about():
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def display_home():
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

# Define the Gradio interface
with gr.Blocks() as demo:
    with gr.Column(visible=True) as home_page:
        gr.Markdown("""
            # Welcome to Wellness Sync
            **Your path to a healthier lifestyle starts here!**
            Take a quick survey and get personalized recommendations for a healthier lifestyle.
        """)
        home_button = gr.Button("Start Survey")
        about_button = gr.Button("About the Makers")

    with gr.Column(visible=False) as form_page:
        gr.Markdown("# Health Monitoring Form")
        gr.Markdown("Please fill out the following information to receive personalized wellness recommendations.")
        
        with gr.Row():
            age = gr.Number(label="Age")
            bmi = gr.Number(label="BMI")
        
        ailments = gr.Textbox(label="Specific ailments")
        food_preference = gr.Textbox(label="Food preference")
        smoker = gr.Textbox(label="Smoker?")
        living_in = gr.Textbox(label="Living in?")
        heriditary_condition = gr.Textbox(label="Any heriditary condition?")
        follow_diet = gr.Textbox(label="Follow Diet")
        
        with gr.Row():
            physical_activity = gr.Number(label="Physical activity")
            sleeping_hours = gr.Number(label="Regular sleeping hours")
        
        alcohol_consumption = gr.Number(label="Alcohol consumption")
        social_interaction = gr.Textbox(label="Social interaction")
        supplements = gr.Textbox(label="Taking supplements")
        mental_health = gr.Textbox(label="Mental health management")
        illness_lastyear = gr.Textbox(label="Illness count last year")
        
        submit = gr.Button("Get Recommendations")
        output = gr.HTML(label="Recommendations", visible=True)
        
        submit.click(fn=handle_user_input, 
                     inputs=[age, bmi, ailments, food_preference, smoker, living_in, heriditary_condition, follow_diet, physical_activity, sleeping_hours, alcohol_consumption, social_interaction, supplements, mental_health, illness_lastyear], 
                     outputs=output)
        
        home_button_in_form = gr.Button("Back to Home")

    with gr.Column(visible=False) as about_page:
        gr.Markdown("""
            # About the Makers
            **Maker 1: Shivam Khosla**  
            **Maker 2: Gauri Bahl**
        """)
        home_button_in_about = gr.Button("Back to Home")

    home_button.click(display_form, outputs=[form_page, about_page, home_page])
    about_button.click(display_about, outputs=[form_page, about_page, home_page])
    home_button_in_form.click(display_home, outputs=[form_page, about_page, home_page])
    home_button_in_about.click(display_home, outputs=[form_page, about_page, home_page])

if __name__ == "__main__":
    demo.launch()
