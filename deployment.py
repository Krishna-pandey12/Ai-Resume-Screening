# import streamlit as st
# import pandas as pd

# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))

# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)

# app.py
# train_model.py
# import streamlit as st
# import pandas as pd
# import joblib

# # 1. Page Configuration (Must be the first Streamlit command)
# st.set_page_config(
#     page_title="AI Resume Screener", 
#     page_icon="🎯", 
#     layout="centered"
# )

# # 2. Custom CSS to style the submit button and layout
# st.markdown("""
#     <style>
#     div.stButton > button:first-child {
#         background-color: #4CAF50;
#         color: white;
#         width: 100%;
#         border-radius: 5px;
#         padding: 10px;
#         font-weight: bold;
#         font-size: 16px;
#     }
#     div.stButton > button:first-child:hover {
#         background-color: #45a049;
#         border-color: #45a049;
#         color: white;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # 3. Header Section
# st.title("🎯 AI Resume Screening Predictor")
# st.markdown("Evaluate candidate profiles instantly based on historical screening data.")
# st.write("Please enter the candidate's metrics below to determine their likelihood of being shortlisted.")
# st.divider()

# try:
#     # Load the saved model and configuration
#     artifact = joblib.load('resume_screening_model.pkl')
#     model = artifact['model']
#     features = artifact['features']
#     edu_mapping = artifact['edu_mapping']

#     # 4. Use a Form for a cleaner UI and to prevent constant reloading
#     with st.form("prediction_form"):
#         st.subheader("Candidate Metrics")
        
#         col1, col2 = st.columns(2)

#         with col1:
#             years_experience = st.number_input("Years of Experience", min_value=0.0, step=0.5, help="Total professional experience in years.")
#             skills_match_score = st.number_input("Skills Match Score (%)", min_value=0.0, max_value=100.0, help="Percentage match with the job description.")
#             edu_level = st.selectbox("Highest Education Level", options=list(edu_mapping.keys()))

#         with col2:
#             project_count = st.number_input("Total Projects", min_value=0, step=1, help="Number of relevant projects completed.")
#             resume_length = st.number_input("Resume Word Count", min_value=0, step=10, help="Total number of words in the resume.")
#             github_activity = st.number_input("GitHub Commits/Activity", min_value=0, step=1, help="Number of recent GitHub contributions or activity score.")

#         st.markdown("<br>", unsafe_allow_html=True)
        
#         # Form submit button
#         submitted = st.form_submit_button("Predict Shortlist Status")

#     # 5. Handle Prediction Display
#     if submitted:
#         input_data = pd.DataFrame([[
#             years_experience,
#             skills_match_score,
#             edu_mapping[edu_level], 
#             project_count,
#             resume_length,
#             github_activity
#         ]], columns=features)
        
#         prediction = model.predict(input_data)[0]
#         probability = model.predict_proba(input_data)[0][1]

#         st.subheader("Prediction Result")
        
#         if prediction == 1:
#             st.success(f"🎉 **Candidate is SHORTLISTED!**")
#             st.info(f"**Confidence Score:** {probability * 100:.2f}%")
#         else:
#             st.error(f"❌ **Candidate is NOT SHORTLISTED.**")
#             st.warning(f"**Confidence Score:** {probability * 100:.2f}%")

# except FileNotFoundError:
#     st.error("⚠️ 'resume_screening_model.pkl' not found. Please run the model training script first to generate the required files.")









import streamlit as st
import pandas as pd
import joblib
from PIL import Image  

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI Resume Screener", 
    page_icon="🎯", 
    layout="centered"
)

# 2. Custom CSS to style the submit button and layout
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        width: 100%;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
        font-size: 16px;
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049;
        border-color: #45a049;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.title("🎯 AI Resume Screening Predictor")
st.markdown("Evaluate candidate profiles instantly based on historical screening data.")
st.write("Please enter the candidate's metrics below to determine their likelihood of being shortlisted.")
st.divider()

try:
    # Load the saved model and configuration
    artifact = joblib.load('resume_screening_model.pkl')
    model = artifact['model']
    features = artifact['features']
    edu_mapping = artifact['edu_mapping']

    # --- Image Upload Section ---
    st.subheader("Candidate Profile Image (Optional)")
    uploaded_image = st.file_uploader("Upload a candidate photo or scanned resume", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        # Open and display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Candidate Image", width=250)
        st.markdown("<br>", unsafe_allow_html=True)

    # 4. Use a Form for a cleaner UI and to prevent constant reloading
    with st.form("prediction_form"):
        st.subheader("Candidate Metrics")
        
        col1, col2 = st.columns(2)

        with col1:
            # UPDATED: Changed min_value to 0 and step to 1 to enforce integer input
            years_experience = st.number_input("Years of Experience", min_value=0, step=1, help="Total professional experience in years.")
            skills_match_score = st.number_input("Skills Match Score (%)", min_value=0.0, max_value=100.0, help="Percentage match with the job description.")
            edu_level = st.selectbox("Highest Education Level", options=list(edu_mapping.keys()))

        with col2:
            project_count = st.number_input("Total Projects", min_value=0, step=1, help="Number of relevant projects completed.")
            resume_length = st.number_input("Resume Word Count", min_value=0, step=10, help="Total number of words in the resume.")
            github_activity = st.number_input("GitHub Commits/Activity", min_value=0, step=1, help="Number of recent GitHub contributions or activity score.")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Form submit button
        submitted = st.form_submit_button("Predict Shortlist Status")

    # 5. Handle Prediction Display
    if submitted:
        input_data = pd.DataFrame([[
            years_experience,
            skills_match_score,
            edu_mapping[edu_level], 
            project_count,
            resume_length,
            github_activity
        ]], columns=features)
        
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        st.subheader("Prediction Result")
        
        if prediction == 1:
            st.success(f"🎉 **Candidate is SHORTLISTED!**")
            st.info(f"**Confidence Score:** {probability * 100:.2f}%")
        else:
            st.error(f"❌ **Candidate is NOT SHORTLISTED.**")
            st.warning(f"**Confidence Score:** {probability * 100:.2f}%")

except FileNotFoundError:
    st.error("⚠️ 'resume_screening_model.pkl' not found. Please run the model training script first to generate the required files.")