import streamlit as st
import utils
import plotly.express as px

choice = st.selectbox("Choose code", utils.codes[:-1])

pet_dict = utils.get_pet_dict()
_ca_dict = utils.get_ca_dict(f'./data/code_docs/{choice}/core_assumptions')
docs = list(pet_dict.keys())

hm_data = utils.get_heatmap_data(choice, docs[0], pet_dict, _ca_dict)

# push to live
# color coding
# add definitions from ppt
for doc in docs:
    hm_data = utils.get_heatmap_data(choice, doc, pet_dict, _ca_dict)
    if len(hm_data) == 0:
        continue
    fig = px.imshow(hm_data, title=doc, text_auto=True)
    st.write(fig)