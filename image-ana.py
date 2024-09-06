import streamlit as st
from pathlib import Path
import google.generativeai as genai

api_key='AIzaSyAEZ0azeHxioW6IBlBnP3niII8RpK9H_mk' # your api key here
genai.configure(api_key=api_key)
generation_config = {
  "temperature": 0.2,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

system_prompt='''

As a medical assistant, you are a cornerstone of the healthcare team, ensuring that the facility runs efficiently and that patients receive the best care possible. 

Your responsibilities include:

1. Detailed Analysis:
   Thoroughly analyze each image, focusing on identifying any abnormalities.

2. Finding Report:
   Document all abnormalities or signs of disease.

3. Recommendations and Next Steps:
   Based on your findings, you provide well-informed recommendations and outline the next steps in the patient care process. 

4. Treatment Suggestions:
   Your input is invaluable in the initial stages. You may suggest potential treatment options based on your analysis, such as medications, physical therapy, or dietary changes. 

5. Requisite Details:
    You should specifically provide the names of the hospitals/medical centres in Kolkata where this disease can be diagnosed.

Important Notes:

1. Scope of Response: Only respond if image pertains to human health issues.

2. Disclaimer: Always consult with a physician before implementing any recommendations or treatment suggestions.

Please provide me an output response with these 6 headings: Detailed Analysis, Finding Report, Recommendations and Next Steps, Treatment Suggestions, Requisite Details, Disclaimer.
'''
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config)

st.set_page_config(
    page_title='MediPal',
    page_icon=':robot:',
    layout='wide',
    initial_sidebar_state='auto'
)

# Custom CSS 
st.markdown("""
    <style>      
    .reportview-container {
        background: #f0f2f6;
        padding: 2rem;
    }
    .sidebar .sidebar-content {
        background: #004aad;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: white;
    }
    .stButton>button {
        background-color: #004aad;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #003080;
    }
    .stImage>img {
        border-radius: 5px;
    }
    .footer {
        background: #004aad;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
    }
    .title {
        color: #004aad;
    }
    .subheader {
        color: #003080;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar content
# st.sidebar.title("MediPal 🤖💉")
# st.sidebar.subheader("Your AI Medical Assistant")

# Main content
st.title("Welcome to Wellnesss Sync💉", anchor=None)
st.markdown("<h2 class='subheader'>An application that helps you analyze medical images.</h2>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload the medical image for analysis", type=['png', 'jpg', 'jpeg'])
if uploaded_file:
    st.image(uploaded_file, width=350, caption="Uploaded Medical Image")

submit_button = st.button("Generate the Analysis")
if submit_button:
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        image_parts = [{'mime_type': 'image/jpeg', 'data': image_data}]
        prompt_parts = [image_parts[0], system_prompt]

        st.markdown("<h2 class='title'>Here is the analysis based on your image:</h2>", unsafe_allow_html=True)
        response = model.generate_content(prompt_parts)
        st.write(response.text)
    else:
        st.error("Please upload an image first.")