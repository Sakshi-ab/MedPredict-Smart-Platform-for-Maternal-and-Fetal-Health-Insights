import os
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import warnings
import pandas as pd
import plotly.express as px
from io import StringIO
import requests


# Debugging: Print the current working directory
print("Current Working Directory:", os.getcwd())

# Debugging: List files in the 'model' folder
if os.path.exists("model"):
    print("Files in 'model' folder:", os.listdir("model"))
else:
    print("'model' folder does not exist")


warnings.filterwarnings("ignore", message="missing ScriptRunContext")

# Ensure the working directory is correct-hardcoding the path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#os.chdir("d:/ML-Project/Maternal_Care") 

from codebase.dashboard_graphs import MaternalHealthDashboard

# Load the models
maternal_Model = pickle.load(open("model/finalized_maternal_model.sav", 'rb'))
fetal_model = pickle.load(open("model/finalized_fetal_model.sav", 'rb'))

# Define the API endpoint
api_endpoint = "https://api.data.gov.in/resource/c6f76dc2-1dac-4d4a-8cc3-db2c7da4579e?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=csv"

# Create an instance of the dashboard
dashboard = MaternalHealthDashboard(maternal_Model, fetal_model, api_endpoint)

#sidebar for navigation
with st.sidebar: 
    st.title("MedPredict")
    st.write("Welcome to the MedPredict")
    st.write("choose an option from the menu below to get started:")
    
    selected = option_menu('MedPredict',
                           ['About us',
                           'Pregnancy Risk Prediction',
                           'Fetal Health Prediction',
                           'Dashboard',],
                            icons=['chat-square-text', 'hospital', 'capsule-pill','clipboard-data'],
                            default_index=0,)

# Main page
if (selected == 'About us'):
    st.title("About us")
    st.title("Welcome to MedPredict")
    st.write("At MedPredict, our Mission is to revoltionize healthcare by offering innovative solutions through the power of AI and machine learning."
             "Our Platform is specifically designed to address the intricate aspects of maternal and fetal health, pregnancy risk prediction, and proactive risk management.")
    col1, col2 = st.columns(2)
    with col1:
        #section 1: Pregnancy Risk Prediction
        st.header("1. Pregnancy Risk Prediction")
        st.write("Our Pregnancy Risk Prediction feature utlize advance algorithm to analyze various health parameters"
                 " Body Sugar levels, Blood Pressure, and more. By processing these information, we provide accurate risk assessment"
                 " to help expectant mothers and healthcare professionals make informed decisions.")
        #Add an image fot Pregnancy Risk Prediction
        st.image("graphics/pregnancy_risk_image.jpg", caption="Pregnancy Risk Prediction", use_container_width=True)
        
    with col2:
        #section 2: Fetal Health Prediction
        st.header("2. Fetal Health Prediction")
        st.write("Fetal Health Prediction is a crucial aspect of our system. we leverage cutting-edge technology to monitor fetal well-being and detect any potential issues early on."
                 "Our algorithms analyze data from Cardiotocograms (CTGs) to provide insights into fetal health status."
                 "we deliver insights into well-being of the unborn child.")
        #Add an image fot Pregnancy Risk Prediction
        st.image("graphics/Fetal_Health_image.jpg", caption="Fetal Health Prediction", use_container_width=True)
        
    #Section 3: Dashboard
    st.header("3. Dashboard")
    st.write("Our Dashboard provides a user-friendly interface for monitoring heath data. It offers visualizations and insights into key health parameters, empowering users to make informed decisions about their health."
             "it is designed to be intuitive and easy to navigate, ensuring that users can access the information they need quickly and efficiently.")
    
        
    #closing note
    
    st.write("Thank you for choosing MedPredict. We are committed to providing you with the best possible experience and helping you achieve your health goals."
             "Feel free to explore our features and take advantage of the insights we provide. If you have any questions or feedback, please don't hesitate to reach out to us.")

if (selected == 'Pregnancy Risk Prediction'):
    st.title("Pregnancy Risk Prediction")
    #Page title
    content = "predicting the risk in pregnancy involves analyzing several parameters, including age, blood sugar, blood pressure, and other health indicators. By inputting these parameters, the model can assess the risk level and provide insights into potential complications during pregnancy."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
    
    #getting th input data from user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.text_input("Age of the person", key = "age")
        
    with col2:
        diastolicBP = st.text_input("Diastolic BP IN mnHg")
        
    with col3:
        BS = st.text_input("Blood glucose in mnol/L")
    
    with col1:
        bodyTemp = st.text_input("Body temperature in Celsius")
        
    with col2:
        heartRate = st.text_input("Heart rate in beats per minute")
        
    
    riskLevel = ""
    predicted_risk = [0]
    
    #creating a button for prediction
    with col1:
        if st.button("Pregnancy Risk Prediction"):
            #creating a button for prediction
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                predicted_risk = maternal_Model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
                #st
                st.subheader("Risk Level")
                if predicted_risk[0] == 0:
                    st.markdown('<bold> <p style="font-weight: bold; font-size: 20px; color: green;"> Low Risk </p></bold>', unsafe_allow_html=True)
                   
                elif predicted_risk[0] == 1:
                     st.markdown('<bold> <p style="font-weight: bold; font-size: 20px; color: orange;"> Medium Risk </p></bold>', unsafe_allow_html=True)
                   
                else:
                     st.markdown('<bold> <p style="font-weight: bold; font-size: 20px; color: red;"> High Risk </p></bold>', unsafe_allow_html=True)
        with col2:
            if st.button("clear"):
                st.rerun()

if (selected == 'Fetal Health Prediction'):
    st.title("Fetal Health Prediction")
    #Page title
    content = "Cardiotocograms(CTGs) are a simple and cost accessible option to assess fetal health, allowing healthcare professionals to take action in order to prevent child and maternal mortality."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
    #getting th input data from user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        BaselineValue = st.text_input("Baseline Value")
        
    with col2:
        Accelerations = st.text_input("Accelerations")
        
    with col3:
        fetal_movement = st.text_input("fetal movement")
    
    with col1:
        uterine_contraction = st.text_input("uterine contraction")
        
    with col2:
        light_declerations = st.text_input("light decelerations")
    
    with col3:
        severe_decelerations = st.text_input("severe decelerations")
    
    with col1:
        prolongued_decelerations = st.text_input("prolongued decelerations")
        
    with col2:
        abnormal_short_term_variability = st.text_input("abnormal short term variability")
    
    with col3:
        mean_value_of_short_term_variability = st.text_input("mean value of short term variability")
        
    with col1:
        percentage_of_time_with_abnormal_long_term_variability = st.text_input("percentage of time with ALTV")
    
    with col2:
        mean_value_of_long_term_variability = st.text_input("mean value of long term variability")
        
    with col3:
        histogram_width = st.text_input("histogram width")
        
    with col1:
        histogram_min = st.text_input("histogram min")
        
    with col2:
        histogram_max = st.text_input("histogram max")
        
    with col3:
        histogram_number_of_peaks = st.text_input("histogram number of peaks")
    
    with col1:
        histogram_number_of_zeroes = st.text_input("histogram number of zeroes")
        
    with col2:
        histogram_mode = st.text_input("histogram mode")
    
    with col3:
        histogram_mean = st.text_input("histogram mean")
    
    with col1:
        histogram_median = st.text_input("histogram median")
        
    with col2:
        histogram_variance = st.text_input("histogram variance")

    with col3:
        histogram_tendency = st.text_input("histogram tendency")           
    
    #creating a button for prediction
    st.markdown('</br>', unsafe_allow_html=True)
    with col1:
        if st.button("predict Pregnancy Risk"):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                predicted_risk = fetal_model.predict([[BaselineValue, Accelerations, fetal_movement,
                                                       uterine_contraction, light_declerations,
                                                       severe_decelerations, prolongued_decelerations,
                                                       abnormal_short_term_variability, mean_value_of_short_term_variability,
                                                       percentage_of_time_with_abnormal_long_term_variability,
                                                       mean_value_of_long_term_variability, histogram_width,
                                                       histogram_min, histogram_max, histogram_number_of_peaks,
                                                       histogram_number_of_zeroes, histogram_mode, histogram_mean,
                                                       histogram_median, histogram_variance, histogram_tendency]])
                
                #st.subheader("Risk Level:")
                st.markdown('</br>', unsafe_allow_html=True)
                if predicted_risk[0] == 0:
                    st.markdown('<bold> <p style="font-weight: bold; font-size: 20px; color: green;">Result comes out to be Normal</p></bold>', unsafe_allow_html=True)
                elif predicted_risk[0] == 1:
                    st.markdown('<bold> <p style="font-weight: bold; font-size: 20px; color: orange;">Result comes out to be Suspect</p></bold>', unsafe_allow_html=True)
                else:
                    st.markdown('<bold> <p style="font-weight: bold; font-size: 20px; color: red;">Result comes out to be Pathological</p></bold>', unsafe_allow_html=True)
                    
        with col2:
            if st.button("clear"):
                st.rerun()
                
if (selected == 'Dashboard'):  
    api_key = "579b464db66ec23bdd000001bb0f7c0a19194f40645d406bd57c3d5e"
    api_endpoint = api_endpoint = f"https://api.data.gov.in/resource/c6f76dc2-1dac-4d4a-8cc3-db2c7da4579e?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=csv"
        
    st.header("Dashboard")
    content = "our interactive dashboard provides a comprehensive overview of maternal health data, allowing users to explore key metrics and trends."
    st.markdown(f"<div style='white-space: pre-wrap;><b>{content}</b></div></br>", unsafe_allow_html=True)
    
    # Create an instance of the dashboard
    dashboard = MaternalHealthDashboard(maternal_Model, fetal_model, api_endpoint)
    # Use the dashboard instance to create the charts
    dashboard.create_bubble_chart()
    with st.expander("Show More"):
    # Display a portion of the data
        content = dashboard.get_bubble_chart_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)

    dashboard.create_pie_chart()
    with st.expander("Show More"):
    # Display a portion of the data
        content = dashboard.get_pie_chart_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)