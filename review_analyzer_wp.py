"""
# Identifying ratings where review's text sentiment is positive, but were accompanied by low ratings
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import demoji # to decode the emoji data
from textblob import TextBlob # for analysing the polarity of review for sentiment gathering
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
        demoji_review = demoji.replace_with_desc(rev, ",") # replace the emoji with its text decription
        demoji_review= re.sub(r'[^\w\s]', '', str(demoji_review)) # cleaning the text
        demoji_review = re.sub(r'\d','',demoji_review)
        demoji_review = demoji_review.lower().strip() # converting text to lower case and stripping head and tail spaces from it
        pol_score = TextBlob(demoji_review).sentiment[0]
        if (pol_score > 0.5): # keeping threshold of 0.5 for positive sentiment
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

def check_password(): ### inspired from streamlit docs
    """ for multiple user authentication"""
    def password_entered():
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
        st.error("password incorrect, please make sure that you entered details right!!!")
        return False
    else:
        return True



def main():
    st.title("Reviews Analyzer")
    # adding style to the page
    html_temp = """
    <div style="background-color:cyan;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Review file analyzer to find low rated reviews with Positive sentiment </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    # to get the interface for uploading, we can use easy streamlit commands
    up_file = st.file_uploader("please upload the Review File for analysis")
    if up_file is not None: ## to validate the file existence
        df = read_df(up_file)
        req_data = gather_req(data=df, columns_req=['ID', 'Text', "Star"])
        req_PosRev_data, req_PosRev_data_full = arrange_data(df, req_data)
        data_csv = req_PosRev_data_full .to_csv().encode('utf-8')
        st.write("## Preview of low rated reviews data set having positive sentiment")
        st.dataframe(req_PosRev_data[['ID', 'Text', 'Star']].head())
        st.write("Click 'Download data as CSV' to download the entire analyzed low rated reviews")
        st.download_button(
             label="Download data as CSV",
             data=data_csv,
             file_name='ngstr_posRev.csv',
             mime='text/csv',
         )

if __name__ == '__main__':
    if check_password():
        main()
