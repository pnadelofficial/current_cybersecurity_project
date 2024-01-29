import streamlit as st
import pickle
import re

st.title("Automatic Tagging Example")

with open('./data/dod_sec_zs_example.p', 'rb') as f:
    data = pickle.load(f)

color_mapping = {
    "Liberalism":"cornflowerblue", 
    "Constructivism":"orange", 
    "Realism":"lightgrey", 
    "Cyber Persistence":"darkorange", 
    "Policy Engineering Tasks":"green"
}

mark_tag = "<mark style='background-color:{color}'>{line}</mark>"

for d in data:
    escape_line = d[0].replace('-', '\-')
    if d[1] != 'No tag':
        color = d[1].split('_')[0]
        c = re.sub(r'\{color\}', color_mapping[color], mark_tag)
        l = re.sub(r'\{line\}', escape_line, c)
        st.markdown(l, unsafe_allow_html=True)
    else:
        st.write(escape_line)