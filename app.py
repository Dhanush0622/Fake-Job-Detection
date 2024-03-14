import streamlit as st
from streamlit_login_auth_ui.widgets import _login_
import streamlit as st 
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

st.set_page_config(page_title = "Real/Fake Job Posting Detection👀")
st.title("Login to use the application")
_loginobj = __login_(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = _login_obj.build_login_ui()
if LOGGED_IN == True:
    # Get the user name.
    fetched_cookies = _login_obj.cookies
    if '_streamlit_login_signup_ui_username_' in fetched_cookies.keys():
        username = fetched_cookies['_streamlit_login_signup_ui_username_']
        st.header(f'Welcome {username} 😀')

        vectorizer = CountVectorizer(max_features=11)
        df = pd.read_csv('fake_job_postings.csv')
        df.dropna(inplace=True)
        st.set_page_config("Deployed App")

        st.title("Fake Job Detection")
        st.header("Enter the Job Description")
        description = st.text_area("Enter or Paste the JD")

        model = pickle.load(open('models/RFC_MODEL.pkl', 'rb'))
        corpus = df['description']
        X = vectorizer.fit_transform(corpus)

        input_data = [description]
        encoded_input = vectorizer.transform([' '.join(input_data)])
        predict_button = st.button("Click to Predict")
        if predict_button:
            predict = model.predict(encoded_input)
            if predict == 0:
                st.write("The Job Posting is Real")
            else:
                st.write("The Job Posting  is Fake")