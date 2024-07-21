# WellnessSync

## 📚 Table of Contents
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Proposed Solution](#proposed-solution)
- [Features & Functionalities](#features--functionalities)
- [Tech Stack](#tech-stack)
- [Project Files Description](#project-files-description)
- [Getting Started](#getting-started)
- [Visualizations](#visualizations)
- [Contributors](#contributors)

## 📝 Project Overview
WellnessSync is designed to gather and analyze data from various sources related to lifestyle, activity, and diet to provide personalized health monitoring. Using machine learning, the project offers predictive health insights and recommendations to help users maintain healthy habits and improve their overall well-being.

## ☁️ Problem Statement
Many existing health monitoring systems face the following challenges:
- **Lack of Personalization:** Generic recommendations that do not consider individual lifestyle factors.
- **Fragmented Data Sources:** Users rely on multiple apps and devices, resulting in incomplete and difficult-to-analyze data.
- **Overwhelming Information:** A plethora of health advice from various sources makes it challenging to discern beneficial information.
- **Inadequate Motivation:** Users struggle to stay motivated without personalized feedback.

## 💾 Proposed Solution
To address these challenges, WellnessSync deploys a machine learning model using joblib for real-time predictions. The project preprocesses and transforms user data to ensure accurate insights and leverages Google Generative AI API for generating tailored health advice.

## Features & Functionalities
- **Personalized Recommendations:** Tailor health and wellness advice to individual users based on unique lifestyle, diet, and activity data.
- **Data Analysis:** Utilize machine learning models to analyze diverse user data.
- **User-Friendly Interface:** Create an engaging and easy-to-use interface that integrates with health apps and devices.

## 📖 Tech Stack
- **Python:** Core programming language
- **Pandas:** For data analysis
- **Flask:** Backend server
- **Scikit-learn:** For building ML models
- **Joblib:** For model persistence
- **Gradio:** For interactive UI
- **Google Generative AI API:** For generating personalized health advice

## 📜 Project Files Description
- `app.py`: Main application file containing the Flask server and Gradio interface.
- `model.pkl`: Trained machine learning model for health predictions.
- `preprocessor.pkl`: Preprocessing pipeline for transforming user data.
- `health_data.zip`: Dataset files used for training and testing the model.
- `Train_Data.csv`: Training dataset.
- `Test_Data.csv`: Testing dataset.

## 🔸 Getting Started
### Prerequisites
- Python 3.x
- Required Python libraries: `pandas`, `joblib`, `gradio`, `flask`, `scikit-learn`, `google-generativeai`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wellnesssync.git
   cd wellnesssync

