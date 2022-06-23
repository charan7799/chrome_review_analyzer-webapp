# -*- coding: utf-8 -*-
"""base_Question_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1khI0C3BgvZPGX5__VbAMy4FnR8LLebvw

# Identifying ratings where review text is good, but rating is negative
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import demoji
from textblob import TextBlob
import streamlit as st

def read_df(file_path):
    df = pd.read_csv(file_path)
    return df

def gather_req(data, columns_req):

    req_data = data[list(columns_req)]
    req_data.describe(include='all')
    req_data.dropna(inplace=True)

    return req_data

def arrange_data(df_org, rev_data, rev_column='Text', rat_column = 'Star'):
    rev_data = rev_data[rev_data[rat_column]==1]
    demoji_text =[]
    rev_sent = []
    for rev in rev_data[rev_column]:
        demoji_review = demoji.replace_with_desc(rev, ",")
        demoji_review= re.sub(r'[^\w\s]', '', str(demoji_review))
        demoji_review = re.sub(r'\d','',demoji_review)
        demoji_review = demoji_review.lower().strip()
        pol_score = TextBlob(demoji_review).sentiment[0]
        if (pol_score > 0.5):
            rev_sent.append('Positive')
        elif (pol_score < 0.5):
            rev_sent.append('Negative')
        else:
            rev_sent.append('Neutral')
        demoji_text.append(demoji_review)

    rev_data['demoji_text'] = demoji_text
    rev_data['sentiment'] = rev_sent
    req_PosRev_data = rev_data[rev_data['sentiment'] == "Positive"]
    req_PosRev_data_full = df_org.loc[df_org['ID'].isin(req_PosRev_data.ID.values)]

    return req_PosRev_data, req_PosRev_data_full

def check_password(): ### took from streamlit docs
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True



def main():
    st.title("review file analyzer")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit review file analyzer webApp </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    up_file = st.file_uploader("please upload the review file")
    if up_file is not None:
        df = read_df(up_file)
        req_data = gather_req(data=df, columns_req=['ID', 'Text', "Star"])
        req_PosRev_data, req_PosRev_data_full = arrange_data(df, req_data)
        data_csv = req_PosRev_data_full .to_csv().encode('utf-8')
        st.write("## preview of the required reviews Data set having ['ID', 'Text', 'Star']")
        st.dataframe(req_PosRev_data[['ID', 'Text', 'Star']].head())
        st.write("Click download data as CSV to download the entire dataset with these required reviews")
        st.download_button(
             label="Download data as CSV",
             data=data_csv,
             file_name='ngstr_posRev.csv',
             mime='text/csv',
         )

if __name__ == '__main__':
    if check_password():
        main()